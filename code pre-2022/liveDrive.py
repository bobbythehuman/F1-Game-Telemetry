from f1_telemetry.server import get_telemetry
from class_dict import digestion, Appendices2
from createPlayers import createPlayer, sessionData

import time
from datetime import datetime
import json
from collections import defaultdict
import keyboard


# keyboard.press("ctrl")
# # release the CTRL button
# keyboard.release("ctrl")

if __name__ == '__main__':
    previous = []

    def press(inputs):
        global previous
        for k in inputs:
            if k in previous:
                previous.remove(k)
            else:
                keyboard.press(k)
        for x in previous:
            keyboard.release(x)
        previous = inputs.copy()

    # f = open('DrivingData.json',"w")

    f = open('DrivingDataCopy.json')
    importedData = json.load(f)
    f.close()
    newImportedData = {}
    for x in importedData.keys():
        newImportedData[float(x)] = importedData[x]

    allData = sessionData()
    players={}
    skip = 0
    skip2 = 50
    startRecord = False

    recordedData = {}
    disData = None
    telData = None
    valid = 0


    print("Server started on 20777")

    print("Start at ",datetime.now().strftime("%a-%d-%b, %H-%M-%S-%f"))

    # packetType = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    for packet, packetID, m_header in get_telemetry([2, 3, 6]):

        if packetID == 2: # players
            data=digestion.ingest_lapdata(packet, m_header)
            if data["m_lapData"][1]["m_lapDistance"] > 0 and not startRecord:
                    startRecord = True
                    print("lap start")
            if startRecord:
                distance = data["m_lapData"][0]["m_lapDistance"]
                inputKeys = []
                try:
                    tel = newImportedData[round(distance,1)]
                    if tel[0] != 0:
                        inputKeys.append("w")
                    if tel[1] != 0:
                        inputKeys.append("s")
                    if tel[2] > 0:
                        inputKeys.append("d")
                    if tel[2] < 0:
                        inputKeys.append("a")
                    press(inputKeys)
                except:
                    pass


                # if valid == 0:
                #     disData = round(distance,0)
                #     valid += 1


        if packetID == 3: # session
            data=digestion.ingest_eventdata(packet, m_header)
            allData.updateEvent(data)
            if data["m_eventStringCode"] == "BUTN":
                buttons = data["m_eventDetails"]["buttons"]["m_buttonStatus"]
                for x in buttons:
                    print(Appendices2.ButtonFlags[x])
                if 0x00100000 in buttons:
                    startRecord=True
                if 0x00200000 in buttons:
                    if skip == 0:
                        startRecord=False
                        break
                    else:
                        skip -= 1

        # if packetID == 6: # players
        #     data=digestion.ingest_cartelemetrydata(packet, m_header)
        #     if startRecord:
        #         if valid == 1:
        #             telData = (data["m_carTelemetryData"][0]["m_throttle"],data["m_carTelemetryData"][0]["m_brake"],data["m_carTelemetryData"][0]["m_steer"])
        #             valid += 1
        #
        # if valid == 2:
        #     recordedData[disData] = telData
        #     disData = None
        #     telData = None
        #     valid = 0
        #     if skip2 == 0:
        #         skip2 = 50
        #         print(len(recordedData.keys()),)
        #     else:
        #         skip2 -= 1


    print("free")
    # f.write(json.dumps(recordedData, ensure_ascii=False, indent=4))
    # f.close()