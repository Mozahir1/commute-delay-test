# Commute alert test

Updated Sun Nov 22 17:58 NY time. First check Tue Nov 17 17:39.

Each check records every MTA alert that could change the trip: delays, planned work and any other
service change on the line. Early checks in this test recorded delays only.

## Did the checks run?

| | Count |
|---|---|
| Checks expected so far | 193 |
| Checks that ran | 193 (100%; the rest GitHub ran more than 30 min late or skipped) |
| MTA unreachable | 0 |
| **Checks with an MTA alert posted** | **41 of 195 (21%)** |

## By line

| Line | Checks | With an alert posted |
|---|---|---|
| 1 | 20 | 7 |
| 6 | 21 | 6 |
| 7 | 20 | 3 |
| A | 20 | 5 |
| E | 21 | 2 |
| F | 13 | 7 |
| G | 20 | 2 |
| L | 20 | 4 |
| N | 20 | 2 |
| Q | 20 | 3 |

## Alerts seen

Proof: [official MTA log](https://data.ny.gov/d/7kct-peq7) links fill in once the MTA publishes the
archive (months behind). [MTA Service Status](https://www.mta.info/) shows an alert only while it's active.

| First seen | Line | MTA alert | MTA event id | Posted by MTA | Official log |
|---|---|---|---|---|---|
| Sun 17:54 | 6 | PLANNED - STOPS SKIPPED: In Manhattan, downtown [4][5][6] skip 86 St | - | Fri 09:43 | - |
| Sun 17:54 | 6 | PLANNED - STOPS SKIPPED: In Manhattan, downtown [4] local and [6] skip 116 St, 110 St, 103 St, 96 St, 77 St, 68 St and 51 St | - | Fri 13:57 | - |
| Sun 17:24 | 7 | PLANNED - STOPS SKIPPED: In Queens, Manhattan-bound [7] skips 111 St, 103 St, 90 St and 82 St All trains at Junction Blvd board from the Flushing-bound platform | - | Fri 11:04 | - |
| Sun 17:24 | 7 | PLANNED - STOPS SKIPPED: In Queens, Flushing-bound [7] skips 52 St and 69 St All trains at Woodside-61 St board from the Manhattan-bound platform | - | Mon 10:18 | - |
| Sun 16:54 | 1 | PLANNED - STOPS SKIPPED: In Manhattan, downtown [1] and [2] local skip 86 St, 79 St, 66 St-Lincoln Center, 59 St-Columbus Circle and 50 St | - | Fri 11:35 | - |
| Sun 16:54 | 1 | PLANNED - STOPS SKIPPED: Downtown [1] skips 125 St | - | Fri 10:24 | - |
| Sun 07:14 | A | DELAYS: Uptown [A] trains are running with delays while we address a signal problem near 88 St. | 277493 | Sun 07:05 | [record](https://data.ny.gov/resource/7kct-peq7.json?event_id=277493) |
| Sat 23:39 | L | DELAYS: Canarsie-Rockaway Pkwy-bound [L] trains are running with delays while we address a signal problem near Bushwick Av/Aberdeen St. | 277469 | Sat 22:58 | [record](https://data.ny.gov/resource/7kct-peq7.json?event_id=277469) |
| Sat 18:34 | A | DELAYS: [A][C] trains are running with delays in both directions after we moved a train that had its brakes activated at 59 St-Columbus Circle. | 277450 | Sat 18:11 | [record](https://data.ny.gov/resource/7kct-peq7.json?event_id=277450) |
| Sat 16:29 | G | DELAYS: [G] trains are running with delays in both directions while we address a switch problem at Court Sq. | 277436 | Sat 14:37 | [record](https://data.ny.gov/resource/7kct-peq7.json?event_id=277436) |
| Sat 13:39 | 6 | REDUCED SERVICE: [6] runs every 8 minutes | - | Fri 12:23 | - |
| Sat 11:09 | 1 | REDUCED SERVICE: [1] runs every 8 minutes | - | Thu 11:29 | - |
| Sat 06:39 | 1 | INFORMATION OUTAGE: Downtown [1] trains are stopping at 116 St-Columbia University, Cathedral Pkwy-110 St, and 103 St, but real-time arrival information may be unavailabl | - | Thu 10:31 | - |
| Fri 22:44 | N | DELAYS: Downtown [N][R] trains are running with delays after we requested EMS for a person in need on a train at 57 St/7 Av. | 277367 | Fri 21:36 | [record](https://data.ny.gov/resource/7kct-peq7.json?event_id=277367) |
| Fri 17:39 | E | DELAYS: [B][D][E] trains are running with delays in both directions. Downtown [C] are running with delays. | 277320 | Fri 15:23 | [record](https://data.ny.gov/resource/7kct-peq7.json?event_id=277320) |
| Fri 16:29 | G | DELAYS: Uptown [F] and Court Sq-bound [G] trains are running with delays after we addressed a door problem on a train at Fort Hamilton Pkwy. | 277332 | Fri 16:18 | [record](https://data.ny.gov/resource/7kct-peq7.json?event_id=277332) |
| Fri 14:14 | Q | DELAYS: [B][Q] trains are running with delays in both directions after we conducted track maintenance in Brooklyn. | 277299 | Fri 11:58 | [record](https://data.ny.gov/resource/7kct-peq7.json?event_id=277299) |
| Fri 12:59 | F | DELAYS: Uptown [F] and Court Sq-bound [G] trains are running with delays after we safely moved crews into place to conduct maintenance near Smith-9 Sts | 277302 | Fri 12:27 | [record](https://data.ny.gov/resource/7kct-peq7.json?event_id=277302) |
| Fri 12:59 | F | DELAYS: Coney Island-Stillwell Av-bound [F] trains are delayed while we conduct track maintenance at W 8 St-NY Aquarium. | 277305 | Fri 12:45 | [record](https://data.ny.gov/resource/7kct-peq7.json?event_id=277305) |
| Fri 07:49 | 7 | DELAYS: 34 St-Hudson Yards-bound [7][7X] trains are running with delays after NYPD responded to people being disruptive on a train at Junction Blvd. | 277263 | Fri 07:08 | [record](https://data.ny.gov/resource/7kct-peq7.json?event_id=277263) |
| Thu 22:14 | E | DELAYS: Uptown [E] trains are running with delays while we perform track maintenance near 5 Av/53 St. | 277204 | Thu 21:04 | [record](https://data.ny.gov/resource/7kct-peq7.json?event_id=277204) |
| Thu 22:14 | E | EXPRESS TO LOCAL: Jamaica-bound [E][F] trains are running local from Jackson Heights-Roosevelt Av to Forest Hills-71 Av. | 277210 | Thu 22:13 | [record](https://data.ny.gov/resource/7kct-peq7.json?event_id=277210) |
| Thu 18:09 | F | DELAYS: [E][F] are running with delays in both directions after we addressed a door problem on a train at Jackson Heights-Roosevelt Av. | 277163 | Thu 17:53 | [record](https://data.ny.gov/resource/7kct-peq7.json?event_id=277163) |
| Thu 14:14 | Q | STOPS SKIPPED: Uptown [Q] trains are running express from Kings Hwy to Prospect Park while FDNY extinguishes a track fire near Parkside Av. | 277127 | Thu 13:54 | [record](https://data.ny.gov/resource/7kct-peq7.json?event_id=277127) |
| Thu 12:59 | F | DELAYS: Coney Island-Stillwell Av-bound [F] and Church Av-bound [G] trains are running with delays after we moved a train that had its brakes activated at Chu | 277121 | Thu 12:41 | [record](https://data.ny.gov/resource/7kct-peq7.json?event_id=277121) |
| Thu 07:04 | L | DELAYS: [L] trains are running with delays in both directions after we investigated what caused a train's brakes to activate near 1 Av. | 277065 | Thu 06:04 | [record](https://data.ny.gov/resource/7kct-peq7.json?event_id=277065) |
| Wed 19:44 | Q | DELAYS: [Q][R] trains are running with delays in both directions after we moved a train that had its brakes activated in the tunnel between Queens and Manhatt | - | - | [search by text](https://data.ny.gov/resource/7kct-peq7.json?%24where=starts_with%28header%2C+%27%5BQ%5D%5BR%5D+trains+are+running+with+delays+in+both+directions+after+we+moved+a+train+%27%29+AND+date+between+%272026-11-17T00%3A00%3A00%27+and+%272026-11-19T23%3A59%3A59%27) |
| Wed 19:04 | N | PART SUSPENDED: No [N][W] trains between Queens and Manhattan. Some uptown [N] trains will end at 57 St/7 Av. Some uptown [W] trains will end at 96 St via the [Q]. | - | - | [search by text](https://data.ny.gov/resource/7kct-peq7.json?%24where=starts_with%28header%2C+%27No+%5BN%5D%5BW%5D+trains+between+Queens+and+Manhattan.+Some+uptown+%5BN%5D+trains+will+end+a%27%29+AND+date+between+%272026-11-17T00%3A00%3A00%27+and+%272026-11-19T23%3A59%3A59%27) |
| Wed 18:49 | L | DELAYS: [L] trains are running with delays in both directions after we moved a train that had its brakes activated near New Lots Av. | - | - | [search by text](https://data.ny.gov/resource/7kct-peq7.json?%24where=starts_with%28header%2C+%27%5BL%5D+trains+are+running+with+delays+in+both+directions+after+we+moved+a+train+tha%27%29+AND+date+between+%272026-11-17T00%3A00%3A00%27+and+%272026-11-19T23%3A59%3A59%27) |
| Wed 18:09 | F | DELAYS: Uptown [F] and Court Sq-bound [G] trains are running with delays after we addressed a mechanical problem on a train near Bergen St. | - | - | [search by text](https://data.ny.gov/resource/7kct-peq7.json?%24where=starts_with%28header%2C+%27Uptown+%5BF%5D+and+Court+Sq-bound+%5BG%5D+trains+are+running+with+delays+after+we+addres%27%29+AND+date+between+%272026-11-17T00%3A00%3A00%27+and+%272026-11-19T23%3A59%3A59%27) |
| Wed 17:54 | 6 | DELAYS: [6] trains are running with delays in both directions Pelham Bay Pk-bound [6X] trains are running with delays. | - | - | [search by text](https://data.ny.gov/resource/7kct-peq7.json?%24where=starts_with%28header%2C+%27%5B6%5D+trains+are+running+with+delays+in+both+directions+Pelham+Bay+Pk-bound+%5B6X%5D+t%27%29+AND+date+between+%272026-11-17T00%3A00%3A00%27+and+%272026-11-19T23%3A59%3A59%27) |
| Wed 13:39 | 6 | DELAYS: [6] trains are delayed entering/leaving Brooklyn Bridge-City Hall while we request EMS assistance for someone on a train at that station. | - | - | [search by text](https://data.ny.gov/resource/7kct-peq7.json?%24where=starts_with%28header%2C+%27%5B6%5D+trains+are+delayed+entering%2Fleaving+Brooklyn+Bridge-City+Hall+while+we+reque%27%29+AND+date+between+%272026-11-17T00%3A00%3A00%27+and+%272026-11-19T23%3A59%3A59%27) |
| Wed 10:29 | A | DELAYS: Downtown [A][C] trains are running with delays following multiple incidents along the lines. | - | - | [search by text](https://data.ny.gov/resource/7kct-peq7.json?%24where=starts_with%28header%2C+%27Downtown+%5BA%5D%5BC%5D+trains+are+running+with+delays+following+multiple+incidents+alon%27%29+AND+date+between+%272026-11-17T00%3A00%3A00%27+and+%272026-11-19T23%3A59%3A59%27) |
| Wed 08:04 | F | DELAYS: [F] trains are running with delays in both directions after we addressed a switch problem near Jay St-MetroTech. | - | - | [search by text](https://data.ny.gov/resource/7kct-peq7.json?%24where=starts_with%28header%2C+%27%5BF%5D+trains+are+running+with+delays+in+both+directions+after+we+addressed+a+switc%27%29+AND+date+between+%272026-11-17T00%3A00%3A00%27+and+%272026-11-19T23%3A59%3A59%27) |
| Wed 07:49 | 7 | DELAYS: [7][7X] trains are running with delays in both directions while we address a mechanical problem on a train at 34 St-Hudson Yards. | - | - | [search by text](https://data.ny.gov/resource/7kct-peq7.json?%24where=starts_with%28header%2C+%27%5B7%5D%5B7X%5D+trains+are+running+with+delays+in+both+directions+while+we+address+a+mec%27%29+AND+date+between+%272026-11-17T00%3A00%3A00%27+and+%272026-11-19T23%3A59%3A59%27) |
| Wed 07:14 | A | SEVERE DELAYS: [A][C][F] trains are running with severe delays in both directions between Manhattan and Brooklyn after we addressed a switch problem near Jay St-Metr | - | - | [search by text](https://data.ny.gov/resource/7kct-peq7.json?%24where=starts_with%28header%2C+%27%5BA%5D%5BC%5D%5BF%5D+trains+are+running+with+severe+delays+in+both+directions+between+Manha%27%29+AND+date+between+%272026-11-17T00%3A00%3A00%27+and+%272026-11-19T23%3A59%3A59%27) |
| Tue 18:49 | L | DELAYS: 8 Av-bound [L] trains are running with delays after we removed a train with a door problem from service at 3 Av. | - | - | [search by text](https://data.ny.gov/resource/7kct-peq7.json?%24where=starts_with%28header%2C+%278+Av-bound+%5BL%5D+trains+are+running+with+delays+after+we+removed+a+train+with+a+do%27%29+AND+date+between+%272026-11-16T00%3A00%3A00%27+and+%272026-11-18T23%3A59%3A59%27) |
| Tue 18:32 | F | DELAYS: Coney island-bound [F] trains are running with delays after we removed a train in need of repairs from service at Kings Hwy. | - | - | [search by text](https://data.ny.gov/resource/7kct-peq7.json?%24where=starts_with%28header%2C+%27Coney+island-bound+%5BF%5D+trains+are+running+with+delays+after+we+removed+a+train+i%27%29+AND+date+between+%272026-11-16T00%3A00%3A00%27+and+%272026-11-18T23%3A59%3A59%27) |

## Latest 20 checks

| Ran | Event | Result |
|---|---|---|
| Sun 17:54 | 6 86 St to Grand Central-42 St 17:55 | 86 St to Grand Central-42 St, 6 in 1 mins / PLANNED - STOPS SKIPPED: In Manhattan, downtown [4][5][6] skip 86 St / PLANNED - STOPS SKIPPED: In Manhattan, downtown [4] local and [6] skip 116 St, 110 St, 103 St, 96 St, 77 St, 68 St and 51 St / REDUCED SERVICE: [6] runs every 8 minutes |
| Sun 17:39 | E Jackson Hts-Roosevelt Av to Lexington Av/53 St 17:40 | Jackson Hts-Roosevelt Av to Lexington Av/53 St, E in 2 mins / no E alerts |
| Sun 17:24 | 7 74 St-Broadway to Grand Central-42 St 17:25 | 74 St-Broadway to Grand Central-42 St, 7 in 1 mins / PLANNED - STOPS SKIPPED: In Queens, Manhattan-bound [7] skips 111 St, 103 St, 90 St and 82 St All trains at Junction Blvd board from the Flushing-bound platform / PLANNED - STOPS SKIPPED: In Queens, Flushing-bound [7] skips 52 St and 69 St All trains at Woodside-61 St board from the Manhattan-bound platform |
| Sun 17:04 | Q Atlantic Av-Barclays Ctr to Canal St 17:05 | Atlantic Av-Barclays Ctr to Canal St, Q in 6 mins / no Q alerts |
| Sun 16:54 | 1 96 St to Times Sq-42 St 16:55 | 96 St to Times Sq-42 St, 1 in 6 mins / PLANNED - STOPS SKIPPED: In Manhattan, downtown [1] and [2] local skip 86 St, 79 St, 66 St-Lincoln Center, 59 St-Columbus Circle and 50 St / PLANNED - STOPS SKIPPED: Downtown [1] skips 125 St / REDUCED SERVICE: [1] runs every 8 minutes |
| Sun 16:29 | G Court Sq to Metropolitan Av 16:30 | Court Sq to Metropolitan Av, G in 0 mins / no G alerts |
| Sun 15:19 | N Queensboro Plaza to Times Sq-42 St 15:20 | Queensboro Plaza to Times Sq-42 St, N in 1 mins / no N delays reported |
| Sun 14:14 | Q Atlantic Av-Barclays Ctr to Canal St 14:15 | Atlantic Av-Barclays Ctr to Canal St, Q in 6 mins / no Q delays reported |
| Sun 13:39 | 6 86 St to Grand Central-42 St 13:40 | 86 St to Grand Central-42 St, 6 in 1 mins / REDUCED SERVICE: [6] runs every 8 minutes |
| Sun 12:29 | 7 74 St-Broadway to Grand Central-42 St 12:30 | 74 St-Broadway to Grand Central-42 St, 7 in 4 mins / no 7 delays reported |
| Sun 12:04 | G Court Sq to Metropolitan Av 12:05 | Court Sq to Metropolitan Av, G in 1 mins / no G delays reported |
| Sun 11:09 | 1 96 St to Times Sq-42 St 11:10 | 96 St to Times Sq-42 St, 1 in 14 mins / INFORMATION OUTAGE: Downtown [1] trains are stopping at 116 St-Columbia University, Cathedral Pkwy-110 St, and 103 St, but real-time arrival information may be unavailabl / REDUCED SERVICE: [1] runs every 8 minutes |
| Sun 10:29 | A 125 St to 59 St-Columbus Circle 10:30 | 125 St to 59 St-Columbus Circle, A in 1 mins / no A delays reported |
| Sun 09:54 | L Bedford Av to 14 St-Union Sq 09:55 | Bedford Av to 14 St-Union Sq, L in 1 mins / no L delays reported |
| Sun 08:44 | E Jackson Hts-Roosevelt Av to Lexington Av/53 St 08:45 | Jackson Hts-Roosevelt Av to Lexington Av/53 St, E in 5 mins / no E delays reported |
| Sun 08:34 | 6 86 St to Grand Central-42 St 08:35 | 86 St to Grand Central-42 St, 6 in 0 mins / no 6 delays reported |
| Sun 08:19 | Q Atlantic Av-Barclays Ctr to Canal St 08:20 | Atlantic Av-Barclays Ctr to Canal St, Q in 11 mins / no Q delays reported |
| Sun 07:49 | 7 74 St-Broadway to Grand Central-42 St 07:50 | 74 St-Broadway to Grand Central-42 St, 7 in 5 mins / no 7 delays reported |
| Sun 07:39 | N Queensboro Plaza to Times Sq-42 St 07:40 | Queensboro Plaza to Times Sq-42 St, N in 8 mins / no N delays reported |
| Sun 07:29 | E Jackson Hts-Roosevelt Av to Lexington Av/53 St 07:30 | Jackson Hts-Roosevelt Av to Lexington Av/53 St, E in 5 mins / no E delays reported |
