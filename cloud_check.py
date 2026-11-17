"""Week-long test runner for GitHub Actions (runs about every 5 minutes; GitHub may run it late).

Each run checks every event in events.csv whose check time (1 minute before start) has passed in
the last 30 minutes and hasn't been checked yet, using the same functions as ui.py, and records
the delays the MTA had posted for that line. Results go to results.jsonl.
"""
import csv
import functools
import json
import os
from datetime import datetime, timedelta

import ui

RESULTS = "results.jsonl"
WINDOW = timedelta(minutes=30)  # a check still runs if GitHub starts the job up to 30 minutes late


def load_events():
    with open("events.csv", newline="") as f:
        return [ui.parse_row(lambda k, r=r: (r.get(k) or "").strip()) for r in csv.DictReader(f)]


def check(ev, now, due):
    rec = {"event": ev["name"], "line": ev["line"], "due": due.isoformat(), "ran": now.isoformat(timespec="seconds")}
    try:
        rec["alerts"] = ui.delays(ev["line"], now)
        rec["message"] = ui.check(ev, now)
    except Exception as e:  # record the failure and keep going with the other events
        rec["error"] = str(e)
    return rec


def main():
    now = datetime.now(ui.TZ)
    ui.STATIONS = ui.load_stations()
    ui.fetch_feed = functools.lru_cache(ui.fetch_feed)  # one download per feed per run
    ui.fetch_alerts = functools.lru_cache(ui.fetch_alerts)
    records = [json.loads(line) for line in open(RESULTS)] if os.path.exists(RESULTS) else []
    done = {(r["event"], r["due"]) for r in records}

    for ev in load_events():
        for day in (now - timedelta(days=1), now):  # yesterday too, for windows that cross midnight
            start = day.replace(hour=ev["start"][0], minute=ev["start"][1], second=0, microsecond=0)
            due = start - timedelta(minutes=1)
            if start.strftime("%a") in ev["days"] and due <= now < due + WINDOW and (ev["name"], due.isoformat()) not in done:
                rec = check(ev, now, due)
                records.append(rec)
                print(f"{now:%Y-%m-%d %H:%M} {ev['name']}: {rec.get('message', rec.get('error'))}")

    with open(RESULTS, "w") as f:
        f.writelines(json.dumps(r) + "\n" for r in records)


if __name__ == "__main__":
    main()
