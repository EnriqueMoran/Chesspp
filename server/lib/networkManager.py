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
        logging.info(f"Network Manager removed.")

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

    def receivedMessage(self, message):    # message = (msg, socket)
        '''
        Message format: TypeID::body
        if TypeID == 0 -> create or join room:
            TypeID::roomId$nick-playerIP
        if TypeID == 1 -> game action:
            TypeID::roomId$messageType-body
        '''
        if len(self.buffer) < self.bufferLen:
            self.buffer.append(message)
            logging.debug(f"Message received:{message[0]}, networkManager buffer len: {len(self.buffer)}.")
        else:
            # send message to client and ask him to retry after x time
            logging.warning(f"Message received but not processed:{message[0]}, buffer has already reached max elements ({len(self.buffer)}).")

    def getMessage(self):    # get oldest received message
        if len(self.buffer) > 0:
            return self.buffer.popleft()
        else:
            return None

    def receiveMessage(self, s=None):
        def receive(connData):
            conn, addr = connData
            with conn:
                print(f"Connected by {addr}")
                while True:
                    try:
                        msg = conn.recv(1024).decode("utf-8")
                        print("received msg: ", msg)
                        if not msg:
                            #break  # if msg = close or similar
                            continue
                        if msg == "close":
                            conn.close()
                            # s.close()
                            logging.debug(f"Connection with {addr} closed.")
                            print(f"Closing connection with {addr}" )
                            break
                        self.receivedMessage((msg, conn))
                    except Exception as e:
                        print(f"Socket error, closing. Error: {e!s}")
                        conn.close()
                print("Socket closed")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    # IPv4, TCP
            s.bind((self.ip, self.port))
            s.listen(5)
            while True: 
                try:
                    t = threading.Thread(target=receive, args=(s.accept(), ))
                    t.start()
                except Exception as e:
                    print(e)
            s.close()
            
    def processResponse(self, response, socket):
        # check if socket
        try:
            socket.sendall(bytes(str(response), "utf-8"))
            logging.debug(f"Message sent: {response}")
        except Exception as e:
            logging.warning(f"Message {response} couldn't be sent. Error: {e!s}.")