from f1_telemetry.server import get_telemetry
from class_dict import digestion
from createPlayers import createPlayer, createPlayer_sort, sessionData

import json
import time
from datetime import datetime


def createFile(location,data):
    fileName=datetime.now().strftime("%a-%d-%b, %H-%M-%S-%f")+".json"
    jsonFile=open(rf"testdata\{location}\{fileName}","w",encoding='utf-8')
    jsonFile.write(json.dumps(data, ensure_ascii=False, indent=4))
    jsonFile.close()

def getDisplay(session, allData):
    qualyFormat = {"pos":0, "status":None, "nationality":None, "name":None, "stops":0, "best":0, "penalty":0}
    raceFormat = {"pos":0, "status":None, "nationality":None, "name":None, "grid":0, "stops":0, "best":0, "raceTime":0, "penalty":0}
    allPlayerData=[]
    for user in allData.values():
        if user.name !="":
            if session in [1, 2, 3, 4]:
                pass
            elif session in [5, 6, 7, 8, 9]:
                dataFormat=qualyFormat.copy()
            elif session in [10, 11, 12]:
                dataFormat=raceFormat.copy()

            playerData=user.getFinal(session)
            dataFormat["pos"]=playerData[0]["m_position"]
            dataFormat["status"]=playerData[0]["m_resultStatus"]
            dataFormat["nationality"]=user.nationality
            dataFormat["name"]=user.name
            dataFormat["stops"]=playerData[0]["m_numPitStops"]
            dataFormat["best"]=playerData[0]["m_bestLapTimeInMs"]
            dataFormat["penalty"]=playerData[0]["m_penaltiesTime"]

            if session in [10, 11, 12]:
                dataFormat["grid"]=playerData[0]["m_gridPosition"]
                dataFormat["raceTime"]=playerData[0]["m_totalRaceTime"]

            allPlayerData.append(dataFormat)
    sortedlist = sorted(allPlayerData, key=lambda d: d['pos'])
    # for x in sortedlist:
    #     print(x)
    return (session,sortedlist)


if __name__ == '__main__':
    allData = sessionData()
    players={}
    session = None
    ready=False
    skip=False
    grid=[]

    print("Server started on 20777")

    print("Start at ",datetime.now().strftime("%a-%d-%b, %H-%M-%S-%f"))

    # packetType = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    for packet, packetID, m_header in get_telemetry():

        if packetID == 0: # players
            data=digestion.ingest_MotionData(packet, m_header)
            if ready:
                for index in range(len(data["m_carMotionData"])):
                    players[index].updateCarMotion(data["m_carMotionData"][index])
            # createFile("motionData",data)

        if packetID == 1: # session
            data=digestion.ingest_sessiondata(packet, m_header)
            session = data["m_sessionType"]
            allData.updateSession(data.copy())
            # createFile("sessionData",data)

        if packetID == 2: # players
            data=digestion.ingest_lapdata(packet, m_header)
            if ready:
                for index in range(len(data["m_lapData"])):
                    players[index].updateLap(data["m_lapData"][index])
                players[data['m_header']['m_playerCarIndex']].updateOtherLap(data)
            # createFile("lapData",data)

        if packetID == 3: # session
            data=digestion.ingest_eventdata(packet, m_header)
            if data['m_eventStringCode'] == "SSTA":
                print("Session has started")
            if data['m_eventStringCode'] == "SEND":
                print("Session has ended")
            # if data["m_eventStringCode"]!="BUTN":
                # createFile("eventData",data)
            allData.updateEvent(data)

        if packetID == 4: # players
            data=digestion.ingest_participantsdata(packet, m_header)
            index = 0
            for player in data['m_participants']:
                player["carIndex"] = index
                if not ready:
                    players[index] = createPlayer_sort(player)
                    allData.updateUserData(player)
                    print(f"{index} - {player['m_name']}")
                players[index].updateParticipants(player)
                index+=1
            allData.updateParticipants(data)
            players[data['m_header']['m_playerCarIndex']].currentPlayer()
            ready=True
            # createFile("participantsData",data)

        if packetID == 5: # players
            data=digestion.ingest_carsetupdata(packet, m_header)
            if ready:
                for index in range(len(data["m_car_setups"])):
                    players[index].updateSetup(data["m_car_setups"][index])
            # createFile("carSetupData",data)

        if packetID == 6: # players
            data=digestion.ingest_cartelemetrydata(packet, m_header)
            if ready:
                for index in range(len(data["m_carTelemetryData"])):
                    players[index].updateTelemetry(data["m_carTelemetryData"][index])
                players[data['m_header']['m_playerCarIndex']].updateOtherTelemetry(data) # check

            # createFile("carTelemetryData",data)

        if packetID == 7: # players
            data=digestion.ingest_carstatusdata(packet, m_header)
            if ready:
                for index in range(len(data["m_carStatusData"])):
                    players[index].updateStatus(data["m_carStatusData"][index])
            # createFile("carStatusData",data)

        if packetID == 8: # players
            if skip == True:
                skip = False
            else:
                skip = True
                data=digestion.ingest_finalclassificationdata(packet, m_header, session)
                if ready:
                    for index in range(len(data["m_classificationData"])):
                        players[index].updateFinal(session,data["m_classificationData"][index])
                # createFile("finalClassificationData",data)
                break

        if packetID == 9: # session
            data=digestion.ingest_lobbyinfodata(packet, m_header)
            if ready:
                for index in range(len(data["m_lobbyPlayers"])):
                    players[index].updateLobbyInfo(data["m_lobbyPlayers"][index])
            allData.updateLobby(data)
            # createFile("lobbyInfoData",data)

        if packetID == 10: # players
            data=digestion.ingest_cardamagedata(packet, m_header)
            if ready:
                for index in range(len(data["m_carDamageData"])):
                    players[index].updateDamage(data["m_carDamageData"][index])
            # createFile("carDamageData",data)

        if packetID == 11: # players
            data=digestion.ingest_sessionhistorydata(packet, m_header)
            if ready:
                index=data["m_carIdx"]
                players[index].updateHistory(data) # check - change
            # createFile("sessionHistoryData",data)

        if packetID == 12: # players
            data=digestion.ingest_tyresetdata(packet, m_header)
            if ready:
                index=data["m_carIdx"]
                players[index].updateTyreSet(data)
            # createFile("tyreSetData",data)

        if packetID == 13: # players - user only
            data=digestion.ingest_motionexdata(packet, m_header)
            if ready:
                players[data['m_header']['m_playerCarIndex']].updateMotionEx(data)
            # createFile("motionExData",data)



    print("free")
