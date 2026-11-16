"""Writes REPORT.md from results.jsonl: did the checks report delays that really happened?

"Late" means 2+ minutes behind the MTA timetable, the same rule ui.py uses.
"Actually late" uses when the train really left the station (its last live prediction before leaving).
"""
import collections
import csv
import json
import statistics
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/New_York")
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def expected_checks(first_due, now):  # every check that should have run between the first one and now
    with open("events.csv", newline="") as f:
        events = list(csv.DictReader(f))
    count, day = 0, first_due.replace(hour=0, minute=0)
    while day <= now:
        for e in events:
            h, m = map(int, e["start"].split(":"))
            due = day.replace(hour=h, minute=m) - timedelta(minutes=1)
            days = e["days"].split() or DAYS
            if first_due <= due and due + timedelta(minutes=30) <= now and (due + timedelta(minutes=1)).strftime("%a") in days:
                count += 1
        day += timedelta(days=1)
    return count


def pct(a, b):
    return f"{100 * a / b:.0f}%" if b else "-"


def main():
    recs = [json.loads(line) for line in open("results.jsonl")]
    now = datetime.now(TZ)
    if not recs:
        open("REPORT.md", "w").write("# Delay check test\n\nNo checks yet.\n")
        return
    first_due = min(datetime.fromisoformat(r["due"]) for r in recs)
    expected = expected_checks(first_due, now)
    done = [r for r in recs if datetime.fromisoformat(r["due"]) + timedelta(minutes=30) <= now]
    trains = [r for r in recs if "predicted" in r]
    timed = [r for r in recs if r.get("reported_late") is not None and "actual_late" in r]
    good = [r for r in timed if r["seconds_between_last_reading_and_departure"] <= 180]  # last reading near departure

    out = [f"# Delay check test\n\nUpdated {now:%a %b %d %H:%M} NY time. First check {first_due:%a %b %d %H:%M}.\n",
           "## Did the checks run?\n", "| | Count |", "|---|---|",
           f"| Checks expected so far | {expected} |",
           f"| Checks that ran | {len(done)} ({pct(len(done), expected)}; the rest GitHub ran more than 30 min late or skipped) |",
           f"| MTA unreachable | {sum('error' in r for r in recs)} |",
           f"| No train found | {sum('message' in r and 'predicted' not in r for r in recs)} |",
           f"| Train not in timetable | {sum(r.get('reported_late') is None for r in trains)} |",
           f"| Train has left, actual time known | {sum('actual' in r for r in recs)} |\n"]

    for title, rows in [("All checks with a known outcome", timed), ("Only where the last reading was within 3 min of departure", good)]:
        both = sum(r["reported_late"] >= 2 and r["actual_late"] >= 2 for r in rows)
        rep = sum(r["reported_late"] >= 2 for r in rows)
        act = sum(r["actual_late"] >= 2 for r in rows)
        err = [abs(r["actual"] - r["predicted"]) / 60 for r in rows]
        out += [f"## Reported vs actual lateness: {title.lower()} ({len(rows)})\n", "| | Count |", "|---|---|",
                f"| Reported late, actually late | {both} |",
                f"| Reported late, actually on time (false alarm) | {rep - both} |",
                f"| Reported on time, actually late (missed) | {act - both} |",
                f"| Reported on time, actually on time | {len(rows) - rep - act + both} |",
                f"| **Correct** | **{pct(len(rows) - (rep - both) - (act - both), len(rows))}** |",
                f"| Departure-time error, median / worst | "
                f"{statistics.median(err):.1f} / {max(err):.1f} min |\n" if err else "| Departure-time error | - |\n"]

    with_alert = [r for r in timed if r.get("alerts")]
    no_alert = [r for r in timed if not r.get("alerts")]
    out += ["## MTA alerts vs actual lateness\n", "| | Checks | Actually late |", "|---|---|---|",
            f"| MTA alert posted for the line | {len(with_alert)} | {pct(sum(r['actual_late'] >= 2 for r in with_alert), len(with_alert))} |",
            f"| No alert posted | {len(no_alert)} | {pct(sum(r['actual_late'] >= 2 for r in no_alert), len(no_alert))} |\n"]

    by_line = collections.defaultdict(list)
    for r in timed:
        by_line[r["line"]].append(r)
    out += ["## By line\n", "| Line | Checks | Avg reported late | Avg actual late | Correct |", "|---|---|---|---|---|"]
    for line, rows in sorted(by_line.items()):
        ok = sum((r["reported_late"] >= 2) == (r["actual_late"] >= 2) for r in rows)
        out.append(f"| {line} | {len(rows)} | {statistics.mean(r['reported_late'] for r in rows):.1f} min | "
                   f"{statistics.mean(r['actual_late'] for r in rows):.1f} min | {pct(ok, len(rows))} |")

    out += ["\n## Latest 20 checks\n", "| Ran | Event | Reported | Actually late |", "|---|---|---|---|"]
    for r in recs[-20:][::-1]:
        actual = f"{r['actual_late']} min" if "actual_late" in r else "waiting" if "last_pred" in r and "actual" not in r else "-"
        out.append(f"| {datetime.fromisoformat(r['ran']):%a %H:%M} | {r['event']} | "
                   f"{(r.get('message') or r.get('error', '')).replace('|', '/')} | {actual} |")
    open("REPORT.md", "w").write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
