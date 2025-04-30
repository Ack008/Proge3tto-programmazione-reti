import socket as sk
import time
import threading
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
def timer():
    while True:
        if timeout >= 0.0:
            time.sleep(1)
            timeout -= 1
        


# Create il socket UDP
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

server_address = ('localhost', 10000)
num_starting_send = 0
ack_received = -1
timeout = 10.0
print("start")
receiving_thread = threading.Thread(target = receive,args= (sock,))
timer_thread = threading.Thread(target = timer)
ack = [True for i in range(WINDOW_LENGHT)]
timer_thread.start()
receiving_thread.start()
first = True
while True:
    if first and num_starting_send == 3:
        first = False
        num_starting_send += 1
    while timeout <= 0.0 or not ack[num_starting_send % WINDOW_LENGHT]:
        message = f"{num_starting_send % WINDOW_LENGHT}packet"
        print("invio ",num_starting_send)
        sock.sendto(message.encode(),server_address)
    
    if timeout > 0 :
        message = f"{num_starting_send % WINDOW_LENGHT}packet"
        print("invio ",num_starting_send)
        sock.sendto(message.encode(),server_address)
        time.sleep(1)
        ack[num_starting_send % WINDOW_LENGHT] = False
        num_starting_send += 1
    else:
        timeout = 10.0
        