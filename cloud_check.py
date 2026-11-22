"""Alert watcher and test runner for GitHub Actions.

Usage: python cloud_check.py [--minutes N]

Does two things:
1. Watches every line in events.csv and sends one phone notification for each alert the MTA posts:
   again only if it changes type (delays -> suspended), or when planned work takes effect again.
   Every alert goes in alerts.jsonl, which is also how it remembers what was already sent.
2. Checks each event whose check time (1 minute before start) has passed in the last 30 minutes,
   using the same functions as ui.py, and records the alerts for that trip in results.jsonl.

With --minutes N it keeps going for N minutes, looking every 30 seconds, and after each new check
or alert updates REPORT.md and pushes the files to GitHub. The workflow runs this for about 5.5 hours, then
starts the next run, so checks happen on time instead of whenever GitHub's schedule fires.
"""
import csv
import functools
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta

import report
import ui

RESULTS = "results.jsonl"
ALERT_LOG = "alerts.jsonl"
WINDOW = timedelta(minutes=30)  # a check still runs if it's found up to 30 minutes late (e.g. between runs)
FETCH_FEED, FETCH_ALERTS = ui.fetch_feed, ui.fetch_alerts


def load_events():
    with open("events.csv", newline="") as f:
        return [ui.parse_row(lambda k, r=r: (r.get(k) or "").strip()) for r in csv.DictReader(f)]


def check(ev, now, due):
    rec = {"event": ev["name"], "line": ev["line"], "due": due.isoformat(), "ran": now.isoformat(timespec="seconds")}
    try:
        rec["alert_details"] = ui.commute_alerts(ev, now)  # MTA ids and times, to match the official archive
        rec["alerts"] = ui.as_text(rec["alert_details"])
        rec["message"], _ = ui.check(ev, now)
    except Exception as e:  # record the failure and keep going with the other events
        rec["error"] = str(e)
    return rec


def check_due(events, records, done):  # runs every check that's due; returns how many ran
    now = datetime.now(ui.TZ)
    count = 0
    for ev in events:
        for day in (now - timedelta(days=1), now):  # yesterday too, for windows that cross midnight
            start = day.replace(hour=ev["start"][0], minute=ev["start"][1], second=0, microsecond=0)
            due = start - timedelta(minutes=1)
            key = (ev["name"], due.isoformat())
            if start.strftime("%a") in ev["days"] and due <= now < due + WINDOW and key not in done:
                rec = check(ev, now, due)
                records.append(rec)
                done.add(key)
                count += 1
                print(f"{now:%Y-%m-%d %H:%M:%S} {ev['name']}: {rec.get('message', rec.get('error'))}", flush=True)
    return count


def watched_lines(events):  # one pseudo-event per line, covering all the stations its events use
    lines = {}
    for ev in events:
        w = lines.setdefault(ev["line"], {"line": ev["line"], "from_ids": set(), "to_ids": set()})
        w["from_ids"] |= ev["from_ids"]
        w["to_ids"] |= ev["to_ids"]
    return list(lines.values())


def load_sent():  # keys of the alerts already handled, or None the very first time
    if not os.path.exists(ALERT_LOG):
        return None
    with open(ALERT_LOG) as f:
        return {json.loads(line)["key"] for line in f}


def alert_message(a):
    when = lambda t: datetime.fromtimestamp(t, ui.TZ).strftime("%a %b %d, %I:%M %p").replace(" 0", " ")
    proof = []
    if a.get("created_at"):
        proof.append(f"MTA posted: {when(a['created_at'])}")
    if a.get("updated_at") and a["updated_at"] != a.get("created_at"):
        proof.append(f"MTA updated: {when(a['updated_at'])}")
    if not a["event_id"] and a["start"]:
        proof.append(f"In effect from: {when(a['start'])}")
    proof.append(f"MTA alert ID: {a['id']}")
    title = f"{', '.join(a['lines'])} {'trains' if len(a['lines']) > 1 else 'train'}: {a['kind']}"
    return title, a["text"] + "\n\n" + "\n".join(proof)


def watch(lines, sent, first_run=False):  # handles every alert not seen before; returns how many
    now = datetime.now(ui.TZ)
    current = {}
    for w in lines:
        for a in ui.commute_alerts(w, now):
            key = a["id"] if a["event_id"] else f"{a['id']}@{a['start']}"  # planned work repeats by date
            current.setdefault(key, {**a, "key": key, "lines": []})["lines"].append(w["line"])
    new = []
    for key, a in current.items():
        if key in sent:
            continue
        notified = False
        if ui.NTFY_TOPIC and not first_run:  # the first run only notes what's already up, without buzzing
            notified = ui.push(*alert_message(a))
            if not notified:
                continue  # not marked as sent, so the next pass sends it
        sent.add(key)
        new.append({**a, "seen": now.isoformat(timespec="seconds"), "notified": notified})
        print(f"{now:%Y-%m-%d %H:%M:%S} new alert on {', '.join(a['lines'])}: {a['kind']}: {a['text']}", flush=True)
    if new or first_run:
        with open(ALERT_LOG, "a") as f:
            f.writelines(json.dumps(a) + "\n" for a in new)
    return len(new)


def save_and_push(records):
    with open(RESULTS, "w") as f:
        f.writelines(json.dumps(r) + "\n" for r in records)
    report.main()
    files = [f for f in (RESULTS, ALERT_LOG, "REPORT.md") if os.path.exists(f)]
    for cmd in (["git", "add", *files], ["git", "commit", "-qm", "Update results"],
                ["git", "pull", "-q", "--rebase"], ["git", "push", "-q"]):
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode:  # e.g. network blip: the next new check or alert pushes again
            print(f"{' '.join(cmd)} failed: {result.stderr.strip() or result.stdout.strip()}", flush=True)
            return


def main():
    minutes = float(sys.argv[sys.argv.index("--minutes") + 1]) if "--minutes" in sys.argv else 0
    stop = time.time() + minutes * 60
    ui.STATIONS = ui.load_stations()
    events = load_events()
    records = [json.loads(line) for line in open(RESULTS)] if os.path.exists(RESULTS) else []
    done = {(r["event"], r["due"]) for r in records}
    print(f"Phone notifications: {'on' if ui.NTFY_TOPIC else 'off (NTFY_TOPIC is not set)'}", flush=True)
    print(f"{datetime.now(ui.TZ):%Y-%m-%d %H:%M:%S} watching {len(events)} events for {minutes:g} minutes", flush=True)
    lines = watched_lines(events)
    sent = load_sent()
    while True:
        ui.fetch_feed = functools.lru_cache(FETCH_FEED)  # fresh data each pass, one download per feed
        ui.fetch_alerts = functools.lru_cache(FETCH_ALERTS)
        changed = 0
        try:
            changed += watch(lines, set() if sent is None else sent, first_run=sent is None)
            if sent is None:
                sent = load_sent()
        except Exception as e:  # keep the loop alive through anything unexpected
            print(f"watch failed: {e}", flush=True)
        try:
            changed += check_due(events, records, done)
            if changed and minutes:
                save_and_push(records)
        except Exception as e:
            print(f"pass failed: {e}", flush=True)
        if time.time() >= stop:
            break
        time.sleep(30)
    if not minutes:
        with open(RESULTS, "w") as f:
            f.writelines(json.dumps(r) + "\n" for r in records)


if __name__ == "__main__":
    main()
