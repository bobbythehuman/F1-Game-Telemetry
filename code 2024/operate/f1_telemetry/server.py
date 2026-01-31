import socket
#import netifaces
import sys
from f1_2024_struct import (PacketHeader, PacketMotionData, PacketSessionData, PacketLapData, PacketEventData, PacketParticipantsData, 
                            PacketCarSetupData, PacketCarTelemetryData, PacketCarStatusData, PacketFinalClassificationData, 
                            PacketLobbyInfoData, PacketCarDamageData, PacketSessionHistoryData, PacketTyreSetsData, PacketMotionExData, PacketTimeTrialData)
from f1_telemetry.f1_2024_struct import *
from digestion import (ingest_Header, ingest_MotionData, ingest_sessiondata, ingest_lapdata, ingest_eventdata, ingest_participantsdata, 
                       ingest_carsetupdata, ingest_cartelemetrydata, ingest_carstatusdata, ingest_finalclassificationdata, 
                       ingest_lobbyinfodata, ingest_cardamagedata, ingest_sessionhistorydata, ingest_tyresetsdata, ingest_motionexdata, ingest_timetrialdata)
from class_dict.digestion import *

#ip_addresses = [netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr'] for iface in netifaces.interfaces() if netifaces.AF_INET in netifaces.ifaddresses(iface)]

UDP_IP = "0.0.0.0"
UDP_PORT = 20777

def get_telemetry():
    print(f"Server started on port {UDP_PORT}")
    #print(f"With an ip of {', '.join(ip_addresses)}")
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, _ = sock.recvfrom(1464) # 1464
        rawPacket= PacketHeader.from_buffer_copy(data[0:32])
        headerPacket = ingest_Header(rawPacket)
        packetID = int(headerPacket.m_packetId)

        match packetID:
            case 0:
                # Frequency: Rate as specified in menus
                rawPacket = PacketMotionData.from_buffer_copy(data[0:1349])
                packet = ingest_MotionData(rawPacket)
            case 1:
                # Frequency: 2 per second
                rawPacket = PacketSessionData.from_buffer_copy(data[0:753])
                packet = ingest_sessiondata(rawPacket)
            case 2:
                # Frequency: Rate as specified in menus
                rawPacket = PacketLapData.from_buffer_copy(data[0:1285])
                packet = ingest_lapdata(rawPacket)
            case 3:
                # Frequency: When the event occurs
                rawPacket = PacketEventData.from_buffer_copy(data[0:45])
                packet = ingest_eventdata(rawPacket)
            case 4:
                # Frequency: Every 5 seconds
                rawPacket = PacketParticipantsData.from_buffer_copy(data[0:1350])
                packet = ingest_participantsdata(rawPacket)
            case 5:
                # Frequency: 2 per second
                rawPacket = PacketCarSetupData.from_buffer_copy(data[0:1133])
                packet = ingest_carsetupdata(rawPacket)
            case 6:
                # Frequency: Rate as specified in menus
                rawPacket = PacketCarTelemetryData.from_buffer_copy(data[0:1352])
                packet = ingest_cartelemetrydata(rawPacket)
            case 7:
                # Frequency: Rate as specified in menus
                rawPacket = PacketCarStatusData.from_buffer_copy(data[0:1239])
                packet = ingest_carstatusdata(rawPacket)
            case 8:
                # Frequency: Once at the end of a race
                rawPacket = PacketFinalClassificationData.from_buffer_copy(data[0:1020])
                packet = ingest_finalclassificationdata(rawPacket)
            case 9:
                # Frequency: Two every second when in the lobby
                rawPacket = PacketLobbyInfoData.from_buffer_copy(data[0:1306])
                packet = ingest_lobbyinfodata(rawPacket)
            case 10:
                # Frequency: 10 per second
                rawPacket = PacketCarDamageData.from_buffer_copy(data[0:953])
                packet = ingest_cardamagedata(rawPacket)
            case 11:
                # Frequency: 20 per second but cycling through cars
                rawPacket = PacketSessionHistoryData.from_buffer_copy(data[0:1460])
                packet = ingest_sessionhistorydata(rawPacket)
            case 12:
                # Frequency: 20 per second but cycling through cars
                rawPacket = PacketTyreSetsData.from_buffer_copy(data[0:231])
                packet = ingest_tyresetsdata(rawPacket)
            case 13:
                # Frequency: Rate as specified in menus
                rawPacket = PacketMotionExData.from_buffer_copy(data[0:237])
                packet = ingest_motionexdata(rawPacket)
            case 14:
                # Frequency: 1 per second
                rawPacket = PacketTimeTrialData.from_buffer_copy(data[0:101])
                packet = ingest_timetrialdata(rawPacket)
            case _:
                packet=None
                header=None

        yield packet, packetID, headerPacket
