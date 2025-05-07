import socket as sk
import time
import threading

WINDOW_LENGTH = 5

class SlidingWindow:
    def __init__(self):
        self.inizialize_var()
        self.timer_lock = threading.Lock()
        self.window_lock = threading.Lock()
    def inizialize_var(self):
        self.window_begin = 0
        self.window_pos = 0
        self.timeout = 10.0
    def receive(self, sock):
        while self.window_begin <= self.lenght:
            data, server = sock.recvfrom(4096)
            num = int(data.decode().split(" ")[0])
            print(f"Received: Ack {num}")
            with self.window_lock:
                self.window_begin += 1

    def timer(self):
        while self.window_begin <= self.lenght:
            time.sleep(1)
            with self.timer_lock:
                if self.timeout > 0:
                    self.timeout -= 1.0
    def start_threads(self):
        self.receiving_thread = threading.Thread(target=sw.receive, args=(sock,))
        self.timer_thread = threading.Thread(target=sw.timer)
        self.receiving_thread.start()
        self.timer_thread.start()
    def wait_threads(self):
        self.timer_thread.join()
        self.receiving_thread.join()

    def send_packets(self, sock, server_address,messageLen):
        self.inizialize_var()
        self.lenght = messageLen
        self.start_threads()
        print(f"Beginning of trasmission : window_begin:{self.window_begin} packets: {self.lenght}")
        print(f"windows_lenght: {WINDOW_LENGTH}")
        while self.window_begin <= self.lenght:
            if self.timeout <= 0.0:
                with self.timer_lock:
                    self.timeout = 10.0
                    self.window_pos = self.window_begin # Reset window_pos after timeout
            elif self.timeout > 0 and self.window_pos <= self.window_begin + WINDOW_LENGTH and self.window_begin <= self.lenght:
                message = f"{self.window_pos} byte"
                print(f"Sending: {self.window_pos}th packet: windows_begin: {self.window_begin}")
                sock.sendto(message.encode(), server_address)
                self.window_pos += 1
                with self.timer_lock:
                    self.timeout = 10.0
                time.sleep(1)
            else:
                print("timer : ",self.timeout)
                time.sleep(1)
        sock.sendto("_".encode(), server_address)
        self.wait_threads()
# Initialize socket and threads
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
server_address = ('localhost', 10000)

sw = SlidingWindow()

# Start threads for receiving and timer


# Start sending packets
sw.send_packets(sock, server_address,30)
sw.send_packets(sock, server_address,20)
