"""Writes REPORT.md from results.jsonl: which delays had the MTA posted at each check?"""
import collections
import csv
import json
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
            start = day.replace(hour=h, minute=m)
            due = start - timedelta(minutes=1)
            if first_due <= due and due + timedelta(minutes=30) <= now and start.strftime("%a") in (e["days"].split() or DAYS):
                count += 1
        day += timedelta(days=1)
    return count


def pct(a, b):
    return f"{100 * a / b:.0f}%" if b else "-"


def main():
    recs = [json.loads(line) for line in open("results.jsonl")]
    now = datetime.now(TZ)
    if not recs:
        open("REPORT.md", "w").write(f"# Delay check test\n\nUpdated {now:%a %b %d %H:%M} NY time. No checks yet.\n")
        return
    first_due = min(datetime.fromisoformat(r["due"]) for r in recs)
    expected = expected_checks(first_due, now)
    ran = [r for r in recs if datetime.fromisoformat(r["due"]) + timedelta(minutes=30) <= now]
    ok = [r for r in recs if "error" not in r]
    delayed = [r for r in ok if r.get("alerts")]

    out = [f"# Delay check test\n\nUpdated {now:%a %b %d %H:%M} NY time. First check {first_due:%a %b %d %H:%M}.\n",
           "Each check records the delays the MTA had posted for the line (delays, suspensions, reroutes,",
           "skipped stops, reduced service; planned work left out).\n",
           "## Did the checks run?\n", "| | Count |", "|---|---|",
           f"| Checks expected so far | {expected} |",
           f"| Checks that ran | {len(ran)} ({pct(len(ran), expected)}; the rest GitHub ran more than 30 min late or skipped) |",
           f"| MTA unreachable | {len(recs) - len(ok)} |",
           f"| **Checks with an MTA delay posted** | **{len(delayed)} of {len(ok)} ({pct(len(delayed), len(ok))})** |\n"]

    by_line = collections.defaultdict(list)
    for r in ok:
        by_line[r["line"]].append(r)
    out += ["## By line\n", "| Line | Checks | With a delay posted |", "|---|---|---|"]
    out += [f"| {line} | {len(rows)} | {sum(bool(r.get('alerts')) for r in rows)} |" for line, rows in sorted(by_line.items())]

    seen = {}  # one row per MTA alert: when we first saw it, its latest text, and links to check it
    for r in ok:
        for a in r.get("alert_details") or [{"id": t, "text": t} for t in r.get("alerts", [])]:  # older checks: text only
            row = seen.setdefault(a.get("event_id") or a["id"], {"first": r["ran"], "lines": set(), **a})
            row["lines"].add(r["line"])
            row.update(text=a["text"], kind=a.get("kind"), updated_at=a.get("updated_at"))
    mta_time = lambda t: f"{datetime.fromtimestamp(t, TZ):%a %H:%M}" if t else "-"
    out += ["\n## Delays seen\n",
            "Proof: [official MTA log](https://data.ny.gov/d/7kct-peq7) links fill in once the MTA publishes the",
            "archive (months behind). [mta.info/alerts](https://www.mta.info/alerts) shows an alert only while it's active.\n",
            "| First seen | Line | MTA alert | MTA event id | Posted by MTA | Official log |", "|---|---|---|---|---|---|"]
    out += [f"| {datetime.fromisoformat(a['first']):%a %H:%M} | {', '.join(sorted(a['lines']))} | "
            f"{a['kind'].upper() + ': ' if a.get('kind') else ''}{a['text'][:150].replace('|', '/')} | {a.get('event_id') or '-'} | "
            f"{mta_time(a.get('created_at'))} | "
            + (f"[record](https://data.ny.gov/resource/7kct-peq7.json?event_id={a['event_id']}) |" if a.get("event_id") else "- |")
            for a in sorted(seen.values(), key=lambda a: a["first"], reverse=True)] or ["| - | - | none yet | - | - | - |"]

    out += ["\n## Latest 20 checks\n", "| Ran | Event | Result |", "|---|---|---|"]
    out += [f"| {datetime.fromisoformat(r['ran']):%a %H:%M} | {r['event']} | {(r.get('message') or r.get('error', '')).replace('|', '/')} |"
            for r in recs[-20:][::-1]]
    open("REPORT.md", "w").write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
