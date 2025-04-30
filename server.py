'''
                            UDP SERVER SOCKET
Corso di Programmazione di Reti - Laboratorio - Università di Bologna
G.Pau - A. Piroddi
'''

import socket as sk
import time
import queue
WINDOW_LENGHT = 5
# Creiamo il socket
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

# associamo il socket alla porta
server_address = ('localhost', 10000)
print ('\n\r starting up on %s port %s' % server_address)

sock.bind(server_address)
window_pos = 0
fiirst=True
while True:
    print('\n\r waiting to receive message...')
    data, address = sock.recvfrom(4096)
    print('received %s bytes from %s' % (len(data), address))
    reck = data.decode() 
    num = int(reck[0])  % WINDOW_LENGHT
    print(f"{num} e {window_pos}")
    window_pos = (window_pos + 1) % WINDOW_LENGHT
    ack=f"{num}"
    time.sleep(1)
    sent = sock.sendto(ack.encode(), address)
    print ('sent %s bytes back to %s' % (sent, address))

