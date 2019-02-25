
#Author: James Bonvivere

import binascii
import socket
import struct
import sys
import hashlib
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5005			#setting the Ip and Port number that will be used to connect to the Server
data = None

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
DataArray = (b'NCC-1701',b'NCC-1664',b'NCC-1017')
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		#create 2 different sockets one for sending the first data
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	#create 2 different sockets one for sending the first data
sock.bind((UDP_IP, 5006))

for x in range(0,3):		#Loop 3 times to run through the 3 different pieces of data to be sent
	print('index', x)
	while True:

		Values = (0,x%2,DataArray[x])       #set ACK bit and Sequence number for packet and the value of that packet
		UDP_Data = struct.Struct('I I 8s')	#Create the structure of the packet with one string that contains all 3 pieces of data
		packed_data = UDP_Data.pack(*Values)
		chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")	#create the checksum

		ValuesChecksum = (0,x%2,DataArray[x],chksum)	#Packet that includes the checksum in order to check if the value is correct when received
		UDP_Packet_Data = struct.Struct('I I 8s 32s')
		UDP_PacketSending = UDP_Packet_Data.pack(*ValuesChecksum)
		
		sock.sendto(UDP_PacketSending, (UDP_IP, UDP_PORT))	#Send the packet via the socket

		try:

			sock2.settimeout(9)					#open the socket and set the timeout so to know if the packet was lost
			data, addr = sock.recvfrom(1024)	
			UDP_PacketCheck = UDP_Packet_Data.unpack(data)	#If packet was received print the packet 
			print(UDP_PacketCheck)

		except :	#except the error for timeout of socket
			if data is None:
				continue		#ACK wasnt sent so retry the sending of this packet

			else:
				UDP_PacketReceived = UDP_Packet_Data.unpack(data)
				values = (UDP_PacketReceived[0],UDP_PacketReceived[1],UDP_PacketReceived[2])
				print(UDP_PacketReceived[0])
				packer = struct.Struct('I I 8s')
				packed_data = packer.pack(*values)
				chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")	#create a new packet without the checksum


				if UDP_PacketReceived[3] == chksum:	#if checksums match then no corruption
					print('Checksum ok')

				else:
					print('corrupt')	#if corruption then retry the sending of this packet
					continue

				if UDP_PacketReceived[1] == (x+1)%2:
					print('Wrong Sequence')				#check the sequence number and if it is incorrect then try packet sending again
					continue


				if UDP_PacketReceived[0]==1:	#if the ACK is received then send the next packet
					print("ACK Received")
					break

				else:
					continue



		if data is None:	#if there is no data there was an issue with the packet reception so retry
			continue

		else:
			UDP_PacketReceived2 = UDP_Packet_Data.unpack(data)	#unpack the packet
			values = (UDP_PacketReceived2[0],UDP_PacketReceived2[1],UDP_PacketReceived2[2]) 
			packer = struct.Struct('I I 8s')
			packed_data = packer.pack(*values)
			chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8") #repack the values without the checksum


		if UDP_PacketReceived2[3] == chksum:
			print('Checksum ok')				#if these match the checksum then packet wasnt corrupt

		else:
			print('corrupt')
			continue

		if UDP_PacketReceived2[1] == (x+1)%2:
			print('Wrong Sequence')				#check sequence number to see if it is correct
			continue


		if UDP_PacketReceived2[0]==1:
			print('ACK Received')		#check if the packet was acknowledged by 
			break
		else:
			continue


sock.close()	#finally close the socket when done 

    
		

