from f1_telemetry.server import get_telemetry
import sys

# from class_dict import digestion
from subModules import eventLog
from enum import Enum
import time
from datetime import datetime


class LatestData:
    def __init__(self):
        self.all = {i: [] for i in range(15)}
        self.MotionData = None
        self.SessionData = None
        self.LapData = None
        self.EventData = None
        self.ParticipantsData = None
        self.CarSetupData = None
        self.CarTelemetryData = None
        self.CarStatusData = None
        self.FinalClassificationData = None
        self.LobbyInfoData = None
        self.CarDamageData = None
        self.SessionHistoryData = None
        self.TyreSetsData = None
        self.MotionExData = None
        self.TimeTrialData = None

    def update(self, packetID, packetData):
        self.all[packetID].append(packetData)
        match packetID:
            case 0:
                self.MotionData = packetData
            case 1:
                self.SessionData = packetData
            case 2:
                self.LapData = packetData
            case 3:
                self.EventData = packetData
            case 4:
                self.ParticipantsData = packetData
            case 5:
                self.CarSetupData = packetData
            case 6:
                self.CarTelemetryData = packetData
            case 7:
                self.CarStatusData = packetData
            case 8:
                self.FinalClassificationData = packetData
            case 9:
                self.LobbyInfoData = packetData
            case 10:
                self.CarDamageData = packetData
            case 11:
                self.SessionHistoryData = packetData
            case 12:
                self.TyreSetsData = packetData
            case 13:
                self.MotionExData = packetData
            case 14:
                self.TimeTrialData = packetData
            case _:
                print("no packet match found")


if __name__ == "__main__":
    latestPackets = LatestData()

    print("Start at ", datetime.now().strftime("%a-%d-%b, %H-%M-%S-%f"))

    dataLogger = eventLog()

    for packet, packetID, m_header in get_telemetry():
        latestPackets.update(packetID, packet)

        dataLogger.LogData(packetID, latestPackets)

        match packetID:
            case 3:
                pass
                # esc = packet.m_eventStringCode
                # if esc in ["SSTA", "SEND", "FTLP", "RTMT", "DRSE", "DRSD", "TMPT", "CHQF", "RCWN", "STLG", "LGOT", "DTSV", "SGSV", "RDFL", "SCAR"]:
                #     print(esc)
            case 1:
                pass

    print("free")
