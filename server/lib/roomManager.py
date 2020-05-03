import uuid
import logging
import threading
from room import Room
from player import Player

class RoomManager:

    def __init__(self, boardData, turnData, messageIdData):
        self.maxRooms = 0
        self.rooms = {}    # make private
        self.boardData = boardData
        self.turnData = turnData
        self.messageIdData = messageIdData
        self.finishedThread = None    # check if any room finished its match
        logging.info(f"Room Manager created.")

    def __repr__(self):
        return f"RoomManager: maxRooms: {self.maxRooms}, activeRooms: {len(self.rooms)}, rooms: {self.rooms})"

    def __str__(self):
        return f"RoomManager: maxRooms: {self.maxRooms}, activeRooms: {len(self.rooms)}, rooms: {list(self.rooms.values())})"

    def loadConfig(self, data):
        self.maxRooms = int(data["max_rooms"])
        self.finishedThread = threading.Thread(target=self.checkFinished)
        self.finishedThread.start()

    def createRoom(self, roomId):    # returns True if room was successfully created, else otherwise
        if len(self.rooms) < self.maxRooms:
            if not roomId in list(self.rooms.keys()):    # if it doesn't already exists
                room = Room(roomId, self.boardData, self.turnData, self.messageIdData)
                self.rooms[roomId] = room
            return True    # room created
        else:
            logging.warning(f"Room {roomId} couldn't be created. Maximun number of rooms ({self.maxRooms}) reached!")
            return False   # couldn't create room

    def addPlayer(self, roomId, player):
        self.rooms[roomId].addPlayer(player)

    def receivedMessage(self, message):
        typeID = int(message.split("::")[0])
        roomId, data = message.split("::")[1].split("$")
        if typeID == 0:    # create or join room
            nick, ip = data.split("-")
            roomCreated = self.createRoom(roomId)
            if roomCreated:
                if(self.rooms[roomId].nPlayers < 2):
                    player = Player(ip, nick, uuid.uuid4())    # create player
                    self.rooms[roomId].addPlayer(player)
                    # send message to client: room created, player id: ...
                else:
                    # send message to client: room already has 2 players
                    logging.debug(f"Room {roomId} player {nick} tried to enter, but room was full!")
                    pass
            else:
                # send message to client: max number of rooms reached
                pass
        elif typeID == 1:
            self.rooms[roomId].receivedMessage(data)

    def checkFinished(self):
        while True:
            if len(self.rooms.keys()) > 0:
                for roomID in list(self.rooms.keys()):    # list casting will avoid runtimeError when modifying keys() items
                    if self.rooms[roomID].finished:
                        self.rooms.pop(roomID)
                        logging.info(f"Removed Room {roomID}.")
            

