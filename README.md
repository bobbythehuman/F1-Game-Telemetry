# F1-Game-Telemetry
Receives telemetry data from the F1 game franchise 

## Documentation
Data output documentations can be found in the `Data Output Doc` folder. <br>
It contains the UDP specifications for the following games:
- F1 25 v3
> [F1 25 UDP Specification Forum](https://forums.ea.com/blog/f1-games-game-info-hub-en/ea-sports%E2%84%A2-f1%C2%AE25-udp-specification/12187347)
- F1 24 v27.2
> [F1 24 UDP Specification Forum](https://forums.ea.com/discussions/f1-24-general-discussion-en/f1-24-udp-specification/8369125)
- F1 23 v29.3
> [F1 23 UDP Specification Forum](https://forums.ea.com/discussions/f1-23-en/f1-23-udp-specification/8390745)
- F1 22 v16
> [F1 21 UDP Specification Forum, has broken download file](https://web.archive.org/web/20230927195200/https://answers.ea.com/t5/General-Discussion/F1-22-UDP-Specification/td-p/11551274)
- F1 21 Not available
> [F1 21 UDP Specification Forum, has broken download file](https://web.archive.org/web/20221203052245/https://forums.codemasters.com/topic/80231-f1-2021-udp-specification/)
- F1 20 v?
> [F1 20 UDP Specification Forum](https://web.archive.org/web/20221127112921/https://forums.codemasters.com/topic/50942-f1-2020-udp-specification/)
- F1 19 v?
> [F1 19 UDP Specification Forum](https://web.archive.org/web/20191115172106/https://forums.codemasters.com/topic/38920-f1-2019-udp-specification/)

## Latest Version
The latest version can be found in `code 2024` <br>
### Main
Inside `main.py` use the following code to retrieve telemetry data:
```
from f1_telemetry.server import get_telemetry
for packet, packetID, m_header in get_telemetry():
     # Your code here
    print(packetID, packet)
```
### Data Storage
If you wish to store the telemetry data you can use the `lastestData` class, making sure to update the class with each packet received:
```
for packet, packetID, m_header in get_telemetry():
    latestPackets.update(packetID, packet)
    # Your code here
```
### Event Logging
If you wish to log events that occur during a session you can use the `eventLogger` class.<br>
make sure to update the class with each event packet received:
```
for packet, packetID, m_header in get_telemetry():
    dataLogger.LogData(packetID, latestPackets)
```
This class will print out to the console any events that occur during a session.<br>
Most event are print as `[{Event Name}] - {message}`
examples include:
- `[SSTA] - Session has started`
- `[FTLP] - User [ID:15-PEREZ-Red Bull Racing-Mexican-11] set fastest lap with [70.744]`
- `[OVTK] - User [ID:16-GASLY-Alpine-French-10] has overtaken [ID:13-RUSSELL-Mercedes-British-63]`
- `[DTSV] - User [ID:19-VERSTAPPEN-Red Bull Racing-Dutch-33] is serving a drive through penalty`
- `[COLL] - Collision between user [ID:15-PEREZ-Red Bull Racing-Mexican-11] and user [ID:17-ALONSO-Aston Martin-Spanish-14]`
- `[RCWN] - User [ID:1-LECLERC-Ferrari-Monegasque-16] has won the race`

It will also create an event log file containing the above events as well as sessions settings, see `code 2024/raceLog.csv` for an example log file. This is created during each event (qualy and race).<br>
At the end of the session it will create a race results file, see `code 2024/raceResults.csv` for an example results file.