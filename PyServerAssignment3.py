import binascii
import socket
import struct
import sys
import hashlib

UDP_IP = "127.0.0.1"
UDP_PORT = 5006
unpacker = struct.Struct('I I 8s 32s')


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, 5005))

for x in range(0,3):
    while True:

        data, addr = sock.recvfrom(1024) 
        UDP_Packet = unpacker.unpack(data)
        print("received from:", addr)
        print("received message:", UDP_Packet)
    
        values = (UDP_Packet[0],UDP_Packet[1],UDP_Packet[2])
        packer = struct.Struct('I I 8s')
        packed_data = packer.pack(*values)
        chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")

        if UDP_Packet[3] == chksum and UDP_Packet[1] == (x%2):
            print('CheckSums Match, Packet OK')
            print(UDP_Packet[0], UDP_Packet[1],UDP_Packet[2])
            values = (1,UDP_Packet[1],UDP_Packet[2])
            UDP_Data = struct.Struct('I I 8s')
            packed_data = UDP_Data.pack(*values)
            chksumSend =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")

            values = (1,UDP_Packet[1],UDP_Packet[2],chksumSend)
            UDP_Packet_Data = struct.Struct('I I 8s 32s')
            UDP_PacketSend = UDP_Packet_Data.pack(*values)
            sock.sendto(UDP_PacketSend, (UDP_IP, UDP_PORT))
            print('Data:  ', UDP_Packet[2].decode('utf-8'))
            break

        else:
            print('Packet Corrupt')
            values = (1,(x+1)%2,UDP_Packet[2])
            UDP_Data = struct.Struct('I I 8s')
            packed_data = UDP_Data.pack(*values)
            chksumSend2 =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")

            values = (1,(x+1)%2,UDP_Packet[2],chksumSend2)
            UDP_Packet_Data = struct.Struct('I I 8s 32s')
            UDP_Packet3 = UDP_Packet_Data.pack(*values)
            
            sock2.sendto(UDP_Packet3, (UDP_IP, UDP_PORT))
            printpack = unpacker.unpack(UDP_Packet3)
            print(printpack)

sock.close()
