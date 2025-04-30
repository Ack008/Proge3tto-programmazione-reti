import socket as sk
import time
import threading
import keyboard as k
global ack_received
global num_starting_send 
global timeout
global WINDOW_LENGHT
global ack
WINDOW_LENGHT = 5

def receive(sock):
    while True:
        data, server = sock.recvfrom(4096)
        num =int(data[0])
        ack[num % WINDOW_LENGHT] = True
        # print(ack)


# Create il socket UDP
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

server_address = ('localhost', 10000)
num_starting_send = 0
ack_received = -1
print("start")
receiving_thread = threading.Thread(target = receive,args= (sock,))
receiving_thread.start()
ack = [True for i in range(WINDOW_LENGHT)]
timeout = 40.0
first = True
while True:
    if first and num_starting_send == 3:
        first = False
        num_starting_send += 1
    while timeout < 0.0 or not ack[num_starting_send % WINDOW_LENGHT]:
        print(ack)
        # pass
    if timeout >= 0 :
        message = f"{num_starting_send % WINDOW_LENGHT}packet"
        print("invio ",num_starting_send)
        sock.sendto(message.encode(),server_address)
        time.sleep(1)
        ack[num_starting_send % WINDOW_LENGHT] = False
        num_starting_send += 1


        
# try:

#     # inviate il messaggio
#     print ('sending "%s"' % message)
#     time.sleep(2) #attende 2 secondi prima di inviare la richiesta
#     sent = sock.sendto(message.encode(), server_address)

#     # Ricevete la risposta dal server
#     print('waiting to receive from')
#     data, server = sock.recvfrom(4096)
#     #print(server)
#     time.sleep(2)
#     print ('received message "%s"' % data.decode('utf8'))
# except Exception as info:
#     print(info)
# finally:
#     print ('closing socket')
#     sock.close()

