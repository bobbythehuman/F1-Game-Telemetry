from f1_telemetry.server import get_telemetry
from class_dict import digestion
from createPlayers import createPlayer, sessionData

import json
import pylab as plt
import time
from datetime import datetime

if __name__ == '__main__':
    allData = sessionData()
    players={}
    session = None
    ready=False
    skip=False


    print("Server started on 20777")

    print("Start at ",datetime.now().strftime("%a-%d-%b, %H-%M-%S-%f"))

    # packetType = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    for packet, packetID, m_header in get_telemetry([1,2,3,4,6,8,10]):

        if packetID == 1: # session
            data=digestion.ingest_sessiondata(packet, m_header)
            session = data["m_sessionType"]
            allData.updateSession(data.copy())
            allData.updateOtherSession(data)

        if packetID == 2: # players
            data=digestion.ingest_lapdata(packet, m_header)
            if ready:
                for index in range(len(data["m_lapData"])):
                    players[index].updateLap(data["m_lapData"][index])

        if packetID == 3: # session
            data=digestion.ingest_eventdata(packet, m_header)
            allData.updateEvent(data)

        if packetID == 4: # players
            data=digestion.ingest_participantsdata(packet, m_header)
            index = 0
            for player in data['m_participants']:
                player["carIndex"] = index
                if not ready:
                    players[index] = createPlayer(player)
                    print(f"{index} - {player['m_name']}")
                players[index].updateParticipants(player)

                index+=1
            allData.updateOtherParticipants(data["m_numActiveCars"])
            players[data['m_header']['m_playerCarIndex']].currentPlayer()
            ready=True

        if packetID == 6: # players
            data=digestion.ingest_cartelemetrydata(packet, m_header)
            if ready:
                for index in range(len(data["m_carTelemetryData"])):
                    players[index].updateTelemetry(data["m_carTelemetryData"][index])
            players[data['m_header']['m_playerCarIndex']].updateOtherTelemetry(data) # check

        if packetID == 8: # players
            if skip == True:
                skip = False
            else:
                skip = True
                data=digestion.ingest_finalclassificationdata(packet, m_header, session)
                if ready:
                    for index in range(len(data["m_classificationData"])):
                        players[index].updateFinal(session,data["m_classificationData"][index])
                break

        if packetID == 10: # players
            data=digestion.ingest_cardamagedata(packet, m_header)
            if ready:
                for index in range(len(data["m_carDamageData"])):
                    players[index].updateDamage(data["m_carDamageData"][index])


    print("free")
    print("extracting data")
    allPlayers=[]
    for x in players.values():
        data=x.toJsonFormat()
        allPlayers.append(data)
        allData.updateUserData(data)
    allDataJson = allData.toJsonFormat()
    print("data extracted")

    print("saving files")
    start=time.time()
    jsonFile=open(rf"testData\allPlayers.json","w",encoding='utf-8')
    jsonFile.write(json.dumps(allPlayers, ensure_ascii=False, indent=4))
    jsonFile.close()
    end=time.time()
    print("allPlayers",end-start)

    start=time.time()
    jsonFile=open(rf"testData\fullRaceData.json","w",encoding='utf-8')
    jsonFile.write(json.dumps(allDataJson, ensure_ascii=False, indent=4))
    jsonFile.close()
    end=time.time()
    print("allRaceData",end-start)

    start=time.time()
    jsonFile=open(rf"testData\PlayerData.json","w",encoding='utf-8')
    jsonFile.write(json.dumps(allPlayers[19], ensure_ascii=False, indent=4))
    jsonFile.close()
    end=time.time()
    print("playerData",end-start)
    print("files saved")
