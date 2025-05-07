'''
                            UDP SERVER SOCKET
Corso di Programmazione di Reti - Laboratorio - Università di Bologna
G.Pau - A. Piroddi
'''

import socket as sk
import time
import random as rd
# Creiamo il socket
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

# associamo il socket alla porta
server_address = ('localhost', 10000)
print ('\n\r starting up on %s port %s' % server_address)

sock.bind(server_address)
num_last_packet = -1
first_time=True
while True:
    data, address = sock.recvfrom(4096)
    if(data.decode() == "_"):
        num_last_packet = - 1
        continue
    print('\n\r waiting to receive message...')
    fails = rd.randint(0,10)
    reck = data.decode().split(" ")[0] 
    num = int(reck)
    if fails != 0:
        print('received %s bytes from %s' % (1, address))
        print(f"received {num}th packet-last packet_received{num_last_packet}")
        if num == num_last_packet + 1:
            num_last_packet += 1
            ack=f"{num}"
            sent = sock.sendto(ack.encode(), address)
            print ('sent %s bytes back to %s' % (sent, address))
    else:
        print(f"{num} not received")
