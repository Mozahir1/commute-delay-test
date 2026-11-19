# Delay check test

Updated Thu Nov 19 07:39 NY time. First check Tue Nov 17 17:39.

Each check records the delays the MTA had posted for the line (delays, suspensions, reroutes,
skipped stops, reduced service; planned work left out).

## Did the checks run?

| | Count |
|---|---|
| Checks expected so far | 58 |
| Checks that ran | 58 (100%; the rest GitHub ran more than 30 min late or skipped) |
| MTA unreachable | 0 |
| **Checks with an MTA delay posted** | **14 of 61 (23%)** |

## By line

| Line | Checks | With a delay posted |
|---|---|---|
| 1 | 6 | 0 |
| 6 | 6 | 2 |
| 7 | 5 | 1 |
| A | 7 | 2 |
| E | 7 | 0 |
| F | 5 | 4 |
| G | 6 | 0 |
| L | 7 | 3 |
| N | 7 | 1 |
| Q | 5 | 1 |

## Delays seen

Proof: [official MTA log](https://data.ny.gov/d/7kct-peq7) links fill in once the MTA publishes the
archive (months behind). [mta.info/alerts](https://www.mta.info/alerts) shows an alert only while it's active.

| First seen | Line | MTA alert | MTA event id | Posted by MTA | Official log |
|---|---|---|---|---|---|
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
| Thu 07:39 | N Queensboro Plaza to Times Sq-42 St 07:40 | Queensboro Plaza to Times Sq-42 St, N in 0 mins / no N delays reported |
| Thu 07:29 | E Jackson Hts-Roosevelt Av to Lexington Av/53 St 07:30 | Jackson Hts-Roosevelt Av to Lexington Av/53 St, E in 0 mins / no E delays reported |
| Thu 07:14 | A 125 St to 59 St-Columbus Circle 07:15 | 125 St to 59 St-Columbus Circle, A in 3 mins / no A delays reported |
| Thu 07:04 | L Bedford Av to 14 St-Union Sq 07:05 | Bedford Av to 14 St-Union Sq, L in 2 mins / DELAYS: [L] trains are running with delays in both directions after we investigated what caused a train's brakes to activate near 1 Av. |
| Thu 06:54 | G Court Sq to Metropolitan Av 06:55 | Court Sq to Metropolitan Av, G in 5 mins / no G delays reported |
| Thu 06:39 | 1 96 St to Times Sq-42 St 06:40 | 96 St to Times Sq-42 St, 1 in 1 mins / no 1 delays reported |
| Wed 23:39 | L Bedford Av to 14 St-Union Sq 23:40 | Bedford Av to 14 St-Union Sq, L in 1 mins / no L delays reported |
| Wed 23:04 | 1 96 St to Times Sq-42 St 23:05 | 96 St to Times Sq-42 St, 1 in 8 mins / no 1 delays reported |
| Wed 22:44 | N Queensboro Plaza to Times Sq-42 St 22:45 | Queensboro Plaza to Times Sq-42 St, N in 8 mins / no N delays reported |
| Wed 22:14 | E Jackson Hts-Roosevelt Av to Lexington Av/53 St 22:15 | Jackson Hts-Roosevelt Av to Lexington Av/53 St, E in 0 mins / no E delays reported |
| Wed 21:49 | 6 86 St to Grand Central-42 St 21:50 | 86 St to Grand Central-42 St, 6 in 5 mins / no 6 delays reported |
| Wed 21:19 | A 125 St to 59 St-Columbus Circle 21:20 | 125 St to 59 St-Columbus Circle, A in 2 mins / no A delays reported |
| Wed 20:39 | 7 74 St-Broadway to Grand Central-42 St 20:40 | 74 St-Broadway to Grand Central-42 St, 7 in 1 mins / no 7 delays reported |
| Wed 20:09 | G Court Sq to Metropolitan Av 20:10 | Court Sq to Metropolitan Av, G in 5 mins / no G delays reported |
| Wed 19:44 | Q Atlantic Av-Barclays Ctr to Canal St 19:45 | Atlantic Av-Barclays Ctr to Canal St, Q in 4 mins / DELAYS: [Q][R] trains are running with delays in both directions after we moved a train that had its brakes activated in the tunnel between Queens and Manhatt |
| Wed 19:04 | N Queensboro Plaza to Times Sq-42 St 19:05 | Queensboro Plaza to Times Sq-42 St, N in 4 mins / PART SUSPENDED: No [N][W] trains between Queens and Manhattan. Some uptown [N] trains will end at 57 St/7 Av. Some uptown [W] trains will end at 96 St via the [Q]. |
| Wed 18:49 | L Bedford Av to 14 St-Union Sq 18:50 | Bedford Av to 14 St-Union Sq, L in 2 mins / DELAYS: [L] trains are running with delays in both directions after we moved a train that had its brakes activated near New Lots Av. |
| Wed 18:34 | A 125 St to 59 St-Columbus Circle 18:35 | 125 St to 59 St-Columbus Circle, A in 4 mins / no A delays reported |
| Wed 18:09 | F Jackson Hts-Roosevelt Av to Lexington Av/53 St 18:10 | Jackson Hts-Roosevelt Av to Lexington Av/53 St, F in 1 mins / DELAYS: Uptown [F] and Court Sq-bound [G] trains are running with delays after we addressed a mechanical problem on a train near Bergen St. |
| Wed 17:54 | 6 86 St to Grand Central-42 St 17:55 | 86 St to Grand Central-42 St, 6 in 5 mins / DELAYS: [6] trains are running with delays in both directions Pelham Bay Pk-bound [6X] trains are running with delays. |
