import binascii
import socket
import struct
import sys
import hashlib
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
data = None

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
DataArray = (b'NCC-1701',b'NCC-1664',b'NCC-1017')
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, 5006))

for x in range(0,3):
	print('index', x)
	while True:

		Values = (0,x%2,DataArray[x])
		UDP_Data = struct.Struct('I I 8s')
		packed_data = UDP_Data.pack(*Values)
		chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")

		ValuesChecksum = (0,x%2,DataArray[x],chksum)
		UDP_Packet_Data = struct.Struct('I I 8s 32s')
		UDP_PacketSending = UDP_Packet_Data.pack(*ValuesChecksum)
		
		sock.sendto(UDP_PacketSending, (UDP_IP, UDP_PORT))

		try:

			sock2.settimeout(9)
			data, addr = sock.recvfrom(1024)
			UDP_PacketCheck = UDP_Packet_Data.unpack(data)
			print(UDP_PacketCheck)

		except :
			if data is None:
				continue

			else:
				UDP_PacketReceived = UDP_Packet_Data.unpack(data)
				values = (UDP_PacketReceived[0],UDP_PacketReceived[1],UDP_PacketReceived[2])
				print(UDP_PacketReceived[0])
				packer = struct.Struct('I I 8s')
				packed_data = packer.pack(*values)
				chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")


				if UDP_PacketReceived[3] == chksum:
					print('Checksum ok')

				else:
					print('corrupt')
					continue

				if UDP_PacketReceived[1] == (x+1)%2:
					print('Wrong Sequence')
					continue


				if UDP_PacketReceived[0]==1:
					print("ACK Received")
					break

				else:
					continue



		if data is None:
			continue

		else:
			UDP_PacketReceived2 = UDP_Packet_Data.unpack(data)
			values = (UDP_PacketReceived2[0],UDP_PacketReceived2[1],UDP_PacketReceived2[2])
			packer = struct.Struct('I I 8s')
			packed_data = packer.pack(*values)
			chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")


		if UDP_PacketReceived2[3] == chksum:
			print('Checksum ok')

		else:
			print('corrupt')
			continue

		if UDP_PacketReceived2[1] == (x+1)%2:
			print('Wrong Sequence')
			continue


		if UDP_PacketReceived2[0]==1:
			print('ACK Received')
			break
		else:
			continue


sock.close()

    
		

