import logging
import socket
import threading
from collections import deque

class NetworkManager:

    def __init__(self):
        self.ip = None
        self.port = None
        self.buffer = deque()
        self.bufferLen = 5    # default size
        self.receiverThread = None    # network data receiver
        logging.info(f"Network Manager created.")

    def __del__(self):
        self.receiverThread.join()

    def __repr__(self):
        return f"networkManager: bufferLen: {self.bufferLen}, buffer: {self.buffer}"

    def __str__(self):
        return f"netWorkManager: buffer len: {len(self.buffer)}, max buffer len: {self.bufferLen}"

    def loadConfig(self, data):
        self.ip = data["ip"]
        self.port = int(data["port"])
        self.bufferLen = int(data["buffer_len"])
        self.receiverThread = threading.Thread(target=self.receiveMessage)
        self.receiverThread.start()

    def receivedMessage(self, message):
        '''
        Message format: TypeID::body
        if TypeID == 0 -> create or join room:
            TypeID::roomId$nick-playerIP
        if TypeID == 1 -> game action:
            TypeID::roomId$messageType-body
        '''
        if len(self.buffer) < self.bufferLen:
            self.buffer.append(message)
            logging.debug(f"Message received:{message}, networkManager buffer len: {len(self.buffer)}.")
        else:
            # send message to client and ask him to retry after x time
            logging.warning(f"Message received but not processed:{message}, buffer has already reached max elements ({len(self.buffer)}).")
            pass

    def getMessage(self):    # get oldest received message
        if len(self.buffer) > 0:
            return self.buffer.popleft()
        else:
            return None

    def receiveMessage(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    # IPv4, TCP
            s.bind((self.ip, self.port))
            s.listen(2)
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    msg = conn.recv(1024).decode("utf-8")
                    if not msg:
                        break
                    print("received msg: ", msg)
                    self.receivedMessage(msg)
                conn.close()
                print("connection closed")