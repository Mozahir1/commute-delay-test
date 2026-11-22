"""Week-long test runner for GitHub Actions.

Usage: python cloud_check.py [--minutes N]

Checks every event in events.csv whose check time (1 minute before start) has passed in the last
30 minutes and hasn't been checked yet, using the same functions as ui.py, and records the alerts
the MTA had posted for that line in results.jsonl. Those alerts also go to the phone (see ui.notify).

With --minutes N it keeps going for N minutes, looking every 30 seconds, and after each new check
updates REPORT.md and pushes both files to GitHub. The workflow runs this for about 5.5 hours, then
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
    ui.fetch_feed = functools.lru_cache(FETCH_FEED)  # fresh data each pass, one download per feed
    ui.fetch_alerts = functools.lru_cache(FETCH_ALERTS)
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
                ui.notify(ev, rec.get("message", ""), rec.get("alert_details", []))
    return count


def save_and_push(records):
    with open(RESULTS, "w") as f:
        f.writelines(json.dumps(r) + "\n" for r in records)
    report.main()
    for cmd in (["git", "add", RESULTS, "REPORT.md"], ["git", "commit", "-qm", "Update results"],
                ["git", "pull", "-q", "--rebase"], ["git", "push", "-q"]):
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode:  # e.g. network blip: the next new check pushes again
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
    while True:
        try:
            if check_due(events, records, done) and minutes:
                save_and_push(records)
        except Exception as e:  # keep the loop alive through anything unexpected
            print(f"pass failed: {e}", flush=True)
        if time.time() >= stop:
            break
        time.sleep(30)
    if not minutes:
        with open(RESULTS, "w") as f:
            f.writelines(json.dumps(r) + "\n" for r in records)


if __name__ == "__main__":
    main()
