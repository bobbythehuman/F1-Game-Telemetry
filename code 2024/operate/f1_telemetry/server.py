import socket
#import netifaces
import sys
from f1_2024_struct import *
from f1_telemetry.f1_2024_struct import *
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
        m_header = PacketHeader.from_buffer_copy(data[0:32])
        packetID = int(m_header.m_packetId)

        match packetID:
            case 0:
                # Frequency: Rate as specified in menus
                packet = PacketMotionData.from_buffer_copy(data[0:1349])
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
                packet = PacketCarSetupData.from_buffer_copy(data[0:1133])
            case 6:
                # Frequency: Rate as specified in menus
                packet = PacketCarTelemetryData.from_buffer_copy(data[0:1352])
            case 7:
                # Frequency: Rate as specified in menus
                packet = PacketCarStatusData.from_buffer_copy(data[0:1239])
            case 8:
                # Frequency: Once at the end of a race
                rawPacket = PacketFinalClassificationData.from_buffer_copy(data[0:1020])
                packet = ingest_finalclassificationdata(rawPacket)
            case 9:
                # Frequency: Two every second when in the lobby
                packet = PacketLobbyInfoData.from_buffer_copy(data[0:1306])
            case 10:
                # Frequency: 10 per second
                packet = PacketCarDamageData.from_buffer_copy(data[0:953])
            case 11:
                # Frequency: 20 per second but cycling through cars
                packet = PacketSessionHistoryData.from_buffer_copy(data[0:1460])
            case 12:
                # Frequency: 20 per second but cycling through cars
                packet = PacketTyreSetsData.from_buffer_copy(data[0:231])
            case 13:
                # Frequency: Rate as specified in menus
                packet = PacketMotionExData.from_buffer_copy(data[0:237])
            case 14:
                # Frequency: 1 per second
                packet = PacketTimeTrialData.from_buffer_copy(data[0:101])
            case _:
                packet=None
                header=None

        yield packet, packetID, m_header
