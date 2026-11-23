"""Commute alert checker, run by GitHub Actions (.github/workflows/checks.yml). Python standard library only.

Reads events.json, which the page in docs/ edits. For each event it looks at the MTA's alerts for the
event's lines 60, 30 and 10 minutes before the start, and sends anything new to the phone through ntfy.sh,
using the topic in the NTFY_TOPIC environment variable. Nothing posted means no notification.

Usage: python3 check.py [--minutes N]   (keeps looking every 30 seconds for N minutes)
"""
import json
import os
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/New_York")
ALERTS = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts.json"
CHECKS = (60, 30, 10)  # minutes before each event
SKIP = ("Station Notice", "Information Outage")  # about single stations, not the line
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
TOPIC = os.environ.get("NTFY_TOPIC", "").strip()


def line_alerts(feed, lines, now):  # alerts on any of these lines that are in effect, or about to be
    found = []
    for ent in feed["entity"]:
        a, ts = ent["alert"], now.timestamp()
        mercury = a.get("transit_realtime.mercury_alert", {})
        mine = [ie for ie in a.get("informed_entity", []) if ie.get("route_id") in lines]
        on = sorted({ie["route_id"] for ie in mine})
        early = mercury.get("display_before_active", 0)  # the MTA shows planned work shortly before it starts
        live = not a.get("active_period") or any(
            int(p.get("start", 0)) - early <= ts and (not p.get("end") or ts <= int(p["end"])) for p in a["active_period"])
        if on and live and mercury.get("alert_type", "") not in SKIP:
            text = next((t["text"] for t in a["header_text"]["translation"] if t["language"] == "en"), "")
            found.append({"id": ent["id"], "lines": on, "kind": mercury.get("alert_type", ""),
                          "text": " ".join(text.split()), "updated": mercury.get("updated_at") or mercury.get("created_at"),
                          "rank": max(int(ie.get("transit_realtime.mercury_entity_selector", {}).get("sort_order", "0").split(":")[-1])
                                      for ie in mine)})  # the MTA's severity: "MTASBWY:E:26" -> 26
    return sorted(found, key=lambda alert: -alert["rank"])  # worst first, so the title names it


def notify(ev, alerts, minutes):  # one phone notification; returns whether ntfy accepted it
    when = lambda t: datetime.fromtimestamp(t, TZ).strftime("%a %I:%M %p") if t else "?"
    more = f" +{len(alerts) - 1} more" if len(alerts) > 1 else ""
    body = {"topic": TOPIC, "click": "https://www.mta.info/",  # tap to compare with the MTA's Service Status
            "title": f"{', '.join(alerts[0]['lines'])} train: {alerts[0]['kind']}{more} ({ev['name']}, {minutes} min)",
            "message": "\n\n".join(f"{a['kind']}: {a['text']}\nMTA updated: {when(a['updated'])}" for a in alerts)[:3500]}
    try:  # the topic goes in the body, not the URL, so it can't show up in an error or a public log
        urllib.request.urlopen(urllib.request.Request("https://ntfy.sh", json.dumps(body).encode()), timeout=10).close()
        return True
    except Exception as e:
        print(f"  notification failed ({e})", flush=True)
        return False


def look(events, now, done, sent):  # runs every check that's due right now
    feed = None
    for ev in events:
        lines = set(ev.get("lines", "").upper().replace(",", " ").split())
        days = [d.strip()[:3].title() for d in ev.get("days", "").replace(",", " ").split()] or DAYS
        h, m = map(int, ev["time"].split(":"))
        for day in (now, now + timedelta(days=1)):  # tomorrow too, for events just after midnight
            start = day.replace(hour=h, minute=m, second=0, microsecond=0)
            for minutes in CHECKS:
                key, due = (ev["name"], start.isoformat(), minutes), start - timedelta(minutes=minutes)
                if start.strftime("%a") not in days or key in done or not due <= now < due + timedelta(minutes=2):
                    continue
                feed = feed or json.load(urllib.request.urlopen(ALERTS, timeout=10))
                seen = sent.setdefault(key[:2], set())  # alerts already sent for this event today
                new = [a for a in line_alerts(feed, lines, now) if a["id"] not in seen]
                if new and TOPIC and not notify(ev, new, minutes):
                    continue  # not marked done, so the next look, 30 seconds later, tries again
                done.add(key)
                seen.update(a["id"] for a in new)
                print(f"{now:%a %H:%M} {ev['name']}, {minutes} min before: "
                      + (" | ".join(f"{a['kind']}: {a['text']}" for a in new) or "nothing new"), flush=True)


def main():
    minutes = float(sys.argv[sys.argv.index("--minutes") + 1]) if "--minutes" in sys.argv else 0
    stop, done, sent = time.time() + minutes * 60, set(), {}
    print(f"Phone notifications: {'on' if TOPIC else 'off (NTFY_TOPIC is not set)'}", flush=True)
    while True:
        subprocess.run(["git", "pull", "-q", "--ff-only"], capture_output=True)  # picks up events saved from the page
        try:
            with open("events.json") as f:
                look(json.load(f), datetime.now(TZ), done, sent)
        except Exception as e:  # e.g. the MTA is unreachable: the next look tries again
            print(f"look failed: {e}", flush=True)
        if time.time() >= stop:
            break
        time.sleep(30)


if __name__ == "__main__":
    main()
