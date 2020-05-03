import logging
import socket
from collections import deque

class NetworkManager:

    def __init__(self):
        self.ip = None
        self.port = None
        # self.socket = None
        self.buffer = deque()
        self.bufferLen = 5
        logging.info(f"Network Manager created.")

    def loadConfig(self, data):
        self.ip = data["ip"]
        self.port = data["port"]
        self.bufferLen = int(data["buffer_len"])

    def connect(self):
        self.host = socket.gethostname() # test
        self.port = 2888 # test

        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.connect((self.host, self.port))
        # send message to check if server is available

    def sendMessage(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    # IPv4, TCP
            s.sendall(bytes(message, "utf-8"))
            logging.debug(f"Message sent: {message}")
            response = s.recv(1024)
            logging.debug(f"Message received: {response}")
            self.buffer.append(response)

    def receivedMessage(self, message):
        if len(self.buffer) < self.bufferLen:
            self.buffer.append(message)
            logging.debug(f"Message received:{message}, networkManager buffer len: {len(self.buffer)}.")
        else:
            # send message to server and ask him to retry after x time
            logging.warning(f"Message received but not processed:{message}, buffer has already reached max elements ({len(self.buffer)}).")
            pass

    def getMessage(self):    # get oldest received message
        if len(self.buffer) > 0:
            return self.buffer.popleft()
        else:
            return None

