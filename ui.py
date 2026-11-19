"""Basic schedule UI. Run: .venv/bin/python3 ui.py, then open http://localhost:8000

Fill in events and press Start. One minute before each event, a background thread prints
when the next train on that line leaves From heading to To, e.g. "Roosevelt to Lex 53rd, E in 4 mins".
"""
import csv
import html
import io
import json
import re
import threading
import time
import urllib.request
import zipfile
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from zoneinfo import ZoneInfo

from google.transit import gtfs_realtime_pb2

TZ = ZoneInfo("America/New_York")
ROWS = 5
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
STOPS_ZIP = "https://rrgtfsfeeds.s3.amazonaws.com/gtfs_subway.zip"  # MTA static data (station names)
FEED = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs"  # live trains, no API key
FEEDS = {"": "1 2 3 4 5 6 6X 7 7X GS", "-ace": "A C E H", "-bdfm": "B D F FS FX M", "-g": "G",
         "-jz": "J Z", "-l": "L", "-nqrw": "N Q R W", "-si": "SI SS"}
LINE_FEED = {line: FEED + suffix for suffix, lines in FEEDS.items() for line in lines.split()}
ALERTS = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts.json"
SKIP = ("Planned", "Station Notice", "Boarding Change", "Extra Service")  # alert types that aren't delays
events = []  # [{"name", "days", "start": (hh, mm), "from", "to", "line", "from_ids", "to_ids"}]


def load_stations():
    data = urllib.request.urlopen(STOPS_ZIP, timeout=60).read()
    stations = {}
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for r in csv.DictReader(io.TextIOWrapper(z.open("stops.txt"), "utf-8-sig")):
            if r["location_type"] == "1":
                stations.setdefault(r["stop_name"], []).append(r["stop_id"])
    return stations


def words(text):  # "Lex 53rd" -> ["lex", "53"]; "Lexington Av/53 St" -> ["lexington", "av", "53", "st"]
    return re.sub(r"(\d+)(st|nd|rd|th)\b", r"\1", text.lower()).replace("/", " ").replace("-", " ").split()


def stop_ids(text):  # every station whose name has a word starting with each typed word
    typed = words(text)
    return {i for name, ids in STATIONS.items()
            if typed and all(any(w.startswith(t) for w in words(name)) for t in typed) for i in ids}


def fetch_feed(line):  # live trains for one line's feed group
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(urllib.request.urlopen(LINE_FEED[line], timeout=10).read())
    return feed


def fetch_alerts():
    return json.load(urllib.request.urlopen(ALERTS, timeout=10))


def next_train(ev, now):  # the MTA's live time for the next train from From toward To, or None
    best = None
    for ent in fetch_feed(ev["line"]).entity:
        tu = ent.trip_update
        if not ent.HasField("trip_update") or tu.trip.route_id != ev["line"]:
            continue
        stops = [(s.stop_id[:-1], s.departure.time or s.arrival.time) for s in tu.stop_time_update]
        for i, (sid, ts) in enumerate(stops):
            if sid in ev["from_ids"] and ts >= now.timestamp() and any(s in ev["to_ids"] for s, _ in stops[i + 1:]):
                best = ts if best is None else min(best, ts)
                break
    return best


def delay_alerts(line, now):  # active unplanned MTA alerts (delays, suspensions, reroutes...) for this line
    found, ts = [], now.timestamp()
    for ent in fetch_alerts()["entity"]:
        a = ent["alert"]
        mercury = a.get("transit_realtime.mercury_alert", {})
        kind = mercury.get("alert_type", "")
        if kind.startswith(SKIP) or not any(ie.get("route_id") == line for ie in a.get("informed_entity", [])):
            continue
        periods = a.get("active_period", [])
        if periods and not any(int(p.get("start", 0)) <= ts and (not p.get("end") or ts <= int(p["end"])) for p in periods):
            continue
        text = next((t["text"] for t in a["header_text"]["translation"] if t["language"] == "en"), "")
        parts = ent["id"].split(":")  # "lmm:alert:277048:26" -> MTA event id 277048 (as in the official archive)
        found.append({"id": ent["id"], "event_id": parts[2] if parts[:2] == ["lmm", "alert"] else None,
                      "kind": kind, "text": " ".join(text.split()),
                      "created_at": mercury.get("created_at"), "updated_at": mercury.get("updated_at")})
    return found


def delays(line, now):  # the same alerts as short lines of text
    return [f"{a['kind'].upper()}: {a['text'][:150]}" for a in delay_alerts(line, now)]


def check(ev, now):
    try:
        ts, found = next_train(ev, now), delays(ev["line"], now)
    except Exception as e:  # keep the background thread alive if the MTA can't be reached
        return f"couldn't reach the MTA ({e})"
    train = (f"{ev['from']} to {ev['to']}, {ev['line']} in {int(ts - now.timestamp()) // 60} mins" if ts
             else f"{ev['from']} to {ev['to']}, no {ev['line']} trains found")
    return f"{train} | " + (" | ".join(found) if found else f"no {ev['line']} delays reported")


def checker():
    fired = set()
    while True:
        now = datetime.now(TZ)
        for ev in list(events):
            if now.strftime("%a") not in ev["days"]:
                continue
            start = now.replace(hour=ev["start"][0], minute=ev["start"][1], second=0, microsecond=0)
            key = (ev["name"], start)
            if start - timedelta(minutes=1) <= now < start and key not in fired:
                fired.add(key)
                print(f"{now:%Y-%m-%d %H:%M:%S} {ev['name']}: {check(ev, now)}", flush=True)
        time.sleep(5)


def parse_row(get):  # get(field) -> the text typed for that field; also used by cloud_check.py
    name = get("name")
    days = [d.strip()[:3].title() for d in get("days").replace(",", " ").split()]
    if any(d not in DAYS for d in days):
        raise ValueError(f"{name}: days must be like Mon,Wed (blank = every day)")
    try:
        t = datetime.strptime(get("start"), "%H:%M")
    except ValueError:
        raise ValueError(f"{name}: time must be 24h HH:MM, e.g. 18:00")
    line = get("line").upper()
    if line not in LINE_FEED:
        raise ValueError(f"{name}: unknown line '{line}' (e.g. E, F, 7)")
    from_ids, to_ids = stop_ids(get("from")), stop_ids(get("to"))
    if not from_ids or not to_ids:
        raise ValueError(f"{name}: no station matches '{get('from') if not from_ids else get('to')}'")
    return {"name": name, "days": days or DAYS, "start": (t.hour, t.minute), "from": get("from"),
            "to": get("to"), "line": line, "from_ids": from_ids, "to_ids": to_ids}


def parse(form):
    parsed = []
    for i in range(ROWS):
        get = lambda field: form.get(f"{field}{i}", [""])[0].strip()
        if get("name"):
            parsed.append(parse_row(get))
    if not parsed:
        raise ValueError("Add at least one event")
    return parsed


def current_values():  # the running events, as the text that goes back in the boxes
    values = {}
    for i, e in enumerate(events):
        values.update({f"name{i}": e["name"], f"days{i}": "" if e["days"] == DAYS else ",".join(e["days"]),
                       f"start{i}": f"{e['start'][0]:02}:{e['start'][1]:02}", f"from{i}": e["from"],
                       f"to{i}": e["to"], f"line{i}": e["line"]})
    return values


def page(message="", values=None):
    values = current_values() if values is None else values
    box = lambda field, i, hint="", extra="": (f'<td><input name="{field}{i}" value="{html.escape(values.get(f"{field}{i}", ""))}"'
                                               f' placeholder="{hint}" {extra}></td>')
    rows = "".join("<tr>" + box("name", i) + box("days", i, "Mon,Wed (blank = every day)") + box("start", i, "HH:MM")
                   + box("from", i, "Roosevelt", 'list="stations"') + box("to", i, "Lex 53rd", 'list="stations"')
                   + box("line", i, "E", 'size="3"') + "</tr>" for i in range(ROWS))
    options = "".join(f'<option value="{html.escape(n)}">' for n in sorted(STATIONS))
    running = "".join(f"<li>{html.escape(e['name'])}: {','.join(e['days'])} at {e['start'][0]:02}:{e['start'][1]:02}, "
                      f"{html.escape(e['from'])} to {html.escape(e['to'])} on the {e['line']}</li>" for e in events)
    return f"""<!doctype html><meta charset="utf-8"><title>Commute schedule</title>
<body style="font-family:sans-serif;max-width:960px;margin:2em auto;padding:0 1em">
<h1>Commute schedule</h1><p>{html.escape(message)}</p>
<form method="post"><table><tr><th>Event</th><th>Days</th><th>Start (24h, NY time)</th><th>From</th><th>To</th>
<th>Line</th></tr>{rows}</table><datalist id="stations">{options}</datalist>
<p><button>Start</button></p></form>
<h2>Running</h2><ul>{running or "<li>Nothing yet</li>"}</ul></body>"""


class Handler(BaseHTTPRequestHandler):
    def respond(self, message="", values=None):
        body = page(message, values).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self.respond()

    def do_POST(self):
        form = parse_qs(self.rfile.read(int(self.headers["Content-Length"])).decode())
        try:
            events[:] = parse(form)
            print(f"started with {len(events)} event(s)", flush=True)
            self.respond(f"Started {len(events)} event(s). Checks run in the background (see the terminal). "
                         "To add one, fill an empty row and press Start; clear a name to remove it.")
        except ValueError as e:  # show what was typed so nothing is lost
            self.respond(f"Not started: {e}", {k: v[0] for k, v in form.items()})

    def log_message(self, *args):  # keep the terminal for check output only
        pass


if __name__ == "__main__":
    print("Loading station names from the MTA...", flush=True)
    STATIONS = load_stations()
    threading.Thread(target=checker, daemon=True).start()
    print("Open http://localhost:8000", flush=True)
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
