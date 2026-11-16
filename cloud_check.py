"""Week-long test runner for GitHub Actions (runs about every 5 minutes; GitHub may run it late).

Each run:
1. Checks every event in events.csv whose check time (1 minute before start) has passed in the
   last 30 minutes and hasn't been checked yet, using the same functions as ui.py.
2. Follows up on earlier checks: while the train is still listed at the station, keep its latest
   predicted time; once it has left, that last prediction is when it actually left.
3. Saves everything to results.jsonl.
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
        nxt = ui.next_train(ev, now)
        rec["alerts"] = ui.delays(ev["line"], now)
        rec["message"] = ui.check(ev, now)
        if nxt:
            ts, trip_id, start_date, stop_id = nxt
            sched = ui.scheduled(trip_id, start_date, stop_id)
            rec.update(trip_id=trip_id, start_date=start_date, stop_id=stop_id, predicted=ts, scheduled=sched,
                       reported_late=None if sched is None else round((ts - sched) / 60),
                       last_pred=ts, last_seen=int(now.timestamp()))
    except Exception as e:  # record the failure and keep going with the other events
        rec["error"] = str(e)
    return rec


def follow_up(rec, now):
    if "last_pred" not in rec or "actual" in rec:
        return
    for ent in ui.fetch_feed(rec["line"]).entity:
        if ent.HasField("trip_update") and ent.trip_update.trip.trip_id == rec["trip_id"]:
            t = next((s.departure.time or s.arrival.time for s in ent.trip_update.stop_time_update
                      if s.stop_id == rec["stop_id"]), None)
            if t:  # still listed at the station: hasn't left yet
                rec["last_pred"], rec["last_seen"] = t, int(now.timestamp())
                return
            break
    rec["actual"] = rec["last_pred"]  # left the station: its last prediction is when it actually left
    rec["seconds_between_last_reading_and_departure"] = rec["last_pred"] - rec["last_seen"]
    if rec.get("scheduled"):
        rec["actual_late"] = round((rec["actual"] - rec["scheduled"]) / 60)


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

    for rec in records:
        try:
            follow_up(rec, now)
        except Exception as e:  # feed down this run: try again next run
            print(f"follow-up failed for {rec['event']}: {e}")

    with open(RESULTS, "w") as f:
        f.writelines(json.dumps(r) + "\n" for r in records)


if __name__ == "__main__":
    main()
