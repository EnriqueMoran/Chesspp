import logging
import socket
import threading
from collections import deque

class NetworkManager:

    def __init__(self):
        self.ip = None
        self.port = None
        # self.socket = None
        self.buffer = deque()
        self.bufferLen = 5
        self.threadPool = []
        logging.info(f"Network Manager created.")

    def __del__(self):
        for t in self.threadPool:
            try:
                t.join(5.0)
            except Exception as e:
                logging.error(f"NetworkManager: thread couldn't be renmoved. Error: {e!s}.")
        logging.info(f"Network Manager removed.")

    def __repr__(self):
        return f"networkManager: bufferLen: {self.bufferLen}, buffer: {self.buffer}, threadPool: {self.threadPool}"

    def __str__(self):
        return f"netWorkManager: buffer len: {len(self.buffer)}, max buffer len: {self.bufferLen}"

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
        def send():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    # IPv4, TCP
                try:
                    s.connect((self.host, self.port))
                    s.sendall(bytes(message, "utf-8"))
                    logging.debug(f"Message sent: {message}")
                    response = int(s.recv(1024).decode("utf-8"))    # response code
                    logging.debug(f"Message received: {response}")
                    s.sendall(bytes("close", "utf-8"))    # tell server to close connection
                    self.buffer.append(response)
                    s.close()
                except Exception as e:
                    logging.error(f"Couldn't stablish connection with server. Error: {e!s}.")
                    print(f"Couldn't stablish connection with server. Error: {e!s}.")
        t = threading.Thread(target=send)
        self.threadPool.append(t)
        t.start()

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

