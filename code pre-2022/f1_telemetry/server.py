import socket

import sys

from f1_2022_struct import *

UDP_IP = "0.0.0.0"
UDP_PORT = 20777

def get_telemetry(packetType = None):
    if packetType is None:
        packetType = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print("started")

    while True:
        data, _ = sock.recvfrom(1464) # 1464
        m_header = PacketHeader.from_buffer_copy(data[0:32])
        packetID = m_header.m_packetId

        if int(packetID) == 0 and int(packetID) in packetType:
            # Frequency: Rate as specified in menus
            packet = PacketMotionData.from_buffer_copy(data[0:1464])

        elif int(packetID) == 1 and int(packetID) in packetType:
            # Frequency: 2 per second
            packet = PacketSessionData.from_buffer_copy(data[0:632])

        elif int(packetID) == 2 and int(packetID) in packetType:
            # Frequency: Rate as specified in menus
            packet = PacketLapData.from_buffer_copy(data[0:972])

        elif int(packetID) == 3 and int(packetID) in packetType:
            # Frequency: When the event occurs
            packet = PacketEventData.from_buffer_copy(data[0:40])

        elif int(packetID) == 4 and int(packetID) in packetType:
            # Frequency: Every 5 seconds
            packet = PacketParticipantsData.from_buffer_copy(data[0:1257])

        elif int(packetID) == 5 and int(packetID) in packetType:
            # Frequency: 2 per second
            packet = PacketCarSetupData.from_buffer_copy(data[0:1102])

        elif int(packetID) == 6 and int(packetID) in packetType:
            # Frequency: Rate as specified in menus
            packet = PacketCarTelemetryData.from_buffer_copy(data[0:1347])

        elif int(packetID) == 7 and int(packetID) in packetType:
            # Frequency: Rate as specified in menus
            packet = PacketCarStatusData.from_buffer_copy(data[0:1058])

        elif int(packetID) == 8 and int(packetID) in packetType:
            # Frequency: Rate as specified in menus
            packet = PacketFinalClassificationData.from_buffer_copy(data[0:1015])

        elif int(packetID) == 9 and int(packetID) in packetType:
            # Frequency: Two every second when in the lobby
            packet = PacketLobbyInfoData.from_buffer_copy(data[0:1191])

        elif int(packetID) == 10 and int(packetID) in packetType:
            # Frequency: 2 per second
            packet = PacketCarDamageData.from_buffer_copy(data[0:948])

        elif int(packetID) == 11 and int(packetID) in packetType:
            # Frequency: 20 per second but cycling through cars
            packet = PacketSessionHistoryData.from_buffer_copy(data[0:1158])

        else:
            packet=None
            theader=None

        yield packet, packetID, m_header

def get_telemetry_non_loop(packetType = None):
    if packetType is None:
        packetType = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    #print("started")

    data, _ = sock.recvfrom(1464) # 1464
    m_header = PacketHeader.from_buffer_copy(data[0:32])
    packetID = m_header.m_packetId

    #sock.shutdown(socket.SHUT_RDWR)
    sock.close()

    if int(packetID) == 0 and int(packetID) in packetType:
        # Frequency: Rate as specified in menus
        packet = PacketMotionData.from_buffer_copy(data[0:1464])

    elif int(packetID) == 1 and int(packetID) in packetType:
        # Frequency: 2 per second
        packet = PacketSessionData.from_buffer_copy(data[0:632])

    elif int(packetID) == 2 and int(packetID) in packetType:
        # Frequency: Rate as specified in menus
        packet = PacketLapData.from_buffer_copy(data[0:972])

    elif int(packetID) == 3 and int(packetID) in packetType:
        # Frequency: When the event occurs
        packet = PacketEventData.from_buffer_copy(data[0:40])

    elif int(packetID) == 4 and int(packetID) in packetType:
        # Frequency: Every 5 seconds
        packet = PacketParticipantsData.from_buffer_copy(data[0:1257])

    elif int(packetID) == 5 and int(packetID) in packetType:
        # Frequency: 2 per second
        packet = PacketCarSetupData.from_buffer_copy(data[0:1102])

    elif int(packetID) == 6 and int(packetID) in packetType:
        # Frequency: Rate as specified in menus
        packet = PacketCarTelemetryData.from_buffer_copy(data[0:1347])

    elif int(packetID) == 7 and int(packetID) in packetType:
        # Frequency: Rate as specified in menus
        packet = PacketCarStatusData.from_buffer_copy(data[0:1058])

    elif int(packetID) == 8 and int(packetID) in packetType:
        # Frequency: Rate as specified in menus
        packet = PacketFinalClassificationData.from_buffer_copy(data[0:1015])

    elif int(packetID) == 9 and int(packetID) in packetType:
        # Frequency: Two every second when in the lobby
        packet = PacketLobbyInfoData.from_buffer_copy(data[0:1191])

    elif int(packetID) == 10 and int(packetID) in packetType:
        # Frequency: 2 per second
        packet = PacketCarDamageData.from_buffer_copy(data[0:948])

    elif int(packetID) == 11 and int(packetID) in packetType:
        # Frequency: 20 per second but cycling through cars
        packet = PacketSessionHistoryData.from_buffer_copy(data[0:1158])

    else:
        packet=None
        theader=None

    yield packet, packetID, m_header