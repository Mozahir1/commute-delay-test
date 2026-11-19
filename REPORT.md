# Delay check test

Updated Thu Nov 19 18:09 NY time. First check Tue Nov 17 17:39.

Each check records the delays the MTA had posted for the line (delays, suspensions, reroutes,
skipped stops, reduced service; planned work left out).

## Did the checks run?

| | Count |
|---|---|
| Checks expected so far | 81 |
| Checks that ran | 81 (100%; the rest GitHub ran more than 30 min late or skipped) |
| MTA unreachable | 0 |
| **Checks with an MTA delay posted** | **17 of 83 (20%)** |

## By line

| Line | Checks | With a delay posted |
|---|---|---|
| 1 | 8 | 0 |
| 6 | 9 | 2 |
| 7 | 8 | 1 |
| A | 8 | 2 |
| E | 9 | 0 |
| F | 9 | 6 |
| G | 8 | 0 |
| L | 8 | 3 |
| N | 8 | 1 |
| Q | 8 | 2 |

## Delays seen

Proof: [official MTA log](https://data.ny.gov/d/7kct-peq7) links fill in once the MTA publishes the
archive (months behind). [mta.info/alerts](https://www.mta.info/alerts) shows an alert only while it's active.

| First seen | Line | MTA alert | MTA event id | Posted by MTA | Official log |
|---|---|---|---|---|---|
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
| Thu 18:09 | F Jackson Hts-Roosevelt Av to Lexington Av/53 St 18:10 | Jackson Hts-Roosevelt Av to Lexington Av/53 St, F in 2 mins / DELAYS: [E][F] are running with delays in both directions after we addressed a door problem on a train at Jackson Heights-Roosevelt Av. |
| Thu 17:54 | 6 86 St to Grand Central-42 St 17:55 | 86 St to Grand Central-42 St, 6 in 1 mins / no 6 delays reported |
| Thu 17:39 | E Jackson Hts-Roosevelt Av to Lexington Av/53 St 17:40 | Jackson Hts-Roosevelt Av to Lexington Av/53 St, E in 2 mins / no E delays reported |
| Thu 17:24 | 7 74 St-Broadway to Grand Central-42 St 17:25 | 74 St-Broadway to Grand Central-42 St, 7 in 1 mins / no 7 delays reported |
| Thu 17:04 | Q Atlantic Av-Barclays Ctr to Canal St 17:05 | Atlantic Av-Barclays Ctr to Canal St, Q in 0 mins / no Q delays reported |
| Thu 16:54 | 1 96 St to Times Sq-42 St 16:55 | 96 St to Times Sq-42 St, 1 in 2 mins / no 1 delays reported |
| Thu 16:29 | G Court Sq to Metropolitan Av 16:30 | Court Sq to Metropolitan Av, G in 2 mins / no G delays reported |
| Thu 15:19 | N Queensboro Plaza to Times Sq-42 St 15:20 | Queensboro Plaza to Times Sq-42 St, N in 13 mins / no N delays reported |
| Thu 14:14 | Q Atlantic Av-Barclays Ctr to Canal St 14:15 | Atlantic Av-Barclays Ctr to Canal St, Q in 1 mins / STOPS SKIPPED: Uptown [Q] trains are running express from Kings Hwy to Prospect Park while FDNY extinguishes a track fire near Parkside Av. |
| Thu 13:39 | 6 86 St to Grand Central-42 St 13:40 | 86 St to Grand Central-42 St, 6 in 3 mins / no 6 delays reported |
| Thu 12:59 | F Jackson Hts-Roosevelt Av to Lexington Av/53 St 13:00 | Jackson Hts-Roosevelt Av to Lexington Av/53 St, F in 3 mins / DELAYS: Coney Island-Stillwell Av-bound [F] and Church Av-bound [G] trains are running with delays after we moved a train that had its brakes activated at Chu |
| Thu 12:29 | 7 74 St-Broadway to Grand Central-42 St 12:30 | 74 St-Broadway to Grand Central-42 St, 7 in 0 mins / no 7 delays reported |
| Thu 12:04 | G Court Sq to Metropolitan Av 12:05 | Court Sq to Metropolitan Av, G in 4 mins / no G delays reported |
| Thu 11:09 | 1 96 St to Times Sq-42 St 11:10 | 96 St to Times Sq-42 St, 1 in 4 mins / no 1 delays reported |
| Thu 10:29 | A 125 St to 59 St-Columbus Circle 10:30 | 125 St to 59 St-Columbus Circle, A in 5 mins / no A delays reported |
| Thu 09:54 | L Bedford Av to 14 St-Union Sq 09:55 | Bedford Av to 14 St-Union Sq, L in 0 mins / no L delays reported |
| Thu 09:19 | F Jackson Hts-Roosevelt Av to Lexington Av/53 St 09:20 | Jackson Hts-Roosevelt Av to Lexington Av/53 St, F in 3 mins / no F delays reported |
| Thu 08:44 | E Jackson Hts-Roosevelt Av to Lexington Av/53 St 08:45 | Jackson Hts-Roosevelt Av to Lexington Av/53 St, E in 2 mins / no E delays reported |
| Thu 08:34 | 6 86 St to Grand Central-42 St 08:35 | 86 St to Grand Central-42 St, 6 in 0 mins / no 6 delays reported |
| Thu 08:19 | Q Atlantic Av-Barclays Ctr to Canal St 08:20 | Atlantic Av-Barclays Ctr to Canal St, Q in 8 mins / no Q delays reported |
