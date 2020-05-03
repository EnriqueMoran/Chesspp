import logging
import threading
import time
from board import Board
from player import Player
from turnManager import TurnManager

class Room:

    def __init__(self, roomId, boardData, turnData, messageTypeData):
        self.id = roomId  # id used to create or join room from client's side
        self.playerOne = None
        self.playerTwo = None
        self.board = None
        self.turnManager = None
        self.boardData = boardData
        self.turnData = turnData
        self.messageTypeData = messageTypeData
        self.loseThread = None    # check if someone losed
        self.finished = False    # did the match finished?
        self.nPlayers = 0
        self.movementId = 0    # message id
        self.exitId = 0
        self.surrenderId = 0
        self.loseId = 0
        self.timeRanOut = 0
        logging.info(f"Room {self.id} created.")

    def __repr__(self):
        if self.nPlayers == 0:
            return f"Room({self.id}): empty"
        elif self.nPlayers == 1:
            return f"Room({self.id}): {self.playerOne.nick}({self.playerOne.id})"
        else:
            return f"Room({self.id}): {self.playerOne.nick}({self.playerOne.id}), {self.playerTwo.nick}({self.playerTwo.id})"

    def loadConfig(self, data):
        self.movementId = int(data["movement"])    # message id
        self.exitId = int(data["exit"])
        self.surrenderId = int(data["surrender"])
        self.loseId = int(data["lose"])
        self.timeRanOut = int(data["time_ran_out"])

    def createBoard(self):
        self.board = Board()
        self.turnManager = TurnManager()
        self.board.loadConfig(self.boardData)
        self.turnManager.loadConfig(self.turnData)

    def addPlayer(self, player):
        if not self.playerOne:
            self.playerOne = player
            self.nPlayers += 1
            logging.info(f"Room {self.id} - player one added: {player}.")
        else:
            self.playerTwo = player
            logging.info(f"Room {self.id} - player two added: {player}.")
            self.nPlayers += 1
            self.createBoard()
            self.board.initialize(self.playerOne.pieces, self.playerTwo.pieces)    # add players pieces
            logging.info(f"Room {self.id} - board initialized.")
            self.play()

    def play(self):
        self.loseThread = threading.Thread(target=self.checkLoser)
        self.loseThread.start()
        self.turnManager.newTurn(0)

    def receivedMessage(self, message):    # format: "type-body"
        messageType = int(message.split("-")[0])
        if messageType == 1:    # receivedMovement  format: movement, elapsedTime
            body = message.split("-")[1]
            movement = body.split(",")[0]
            elapsedTime = int(body.split(",")[1])
            self.turnManager.receivedMovement(movement, elapsedTime)
        elif messageType == 2:    # receivedExit
            self.turnManager.receivedExit()
        elif messageType == 3:    # receivedSurrender
            self.turnManager.receivedSurrender()
        elif messageType == 4:    # receivedLose
            self.turnManager.receivedLose()
        elif messageType == 5:    # receivedTimeRanOut
            self.turnManager.receivedTimeRanOut()

    def checkLoser(self):
        while True:
            lose, loser, message = self.turnManager.lose
            if lose:
                print(message.replace("0", self.playerOne.nick).replace("1", self.playerTwo.nick))
                if loser == 0:                 
                    print(f"{self.playerTwo.nick} win!")
                    logging.info(f"Room {self.id} - Match finished, {self.playerTwo.nick} won.")
                else:
                    print(f"{self.playerOne.nick} win!")
                    logging.info(f"Room {self.id} - Match finished, {self.playerOne.nick} won.")
                break
            time.sleep(1)
        self.finished = True    # match finished, tell networkManager to delete this room
        return