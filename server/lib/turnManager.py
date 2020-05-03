import threading

class TurnManager:

    def __init__(self):
        self.movsRepeated = 0    # number of identical movements before match ends (client side)
        self.maxMovs = 0    # number of movements without capturing (client side)
        self.playerOneTimer = 0    # time per player before match ends
        self.playerTwoTimer = 0
        self.timeout = 0    # timeout defeat
        self.timeThread = None    # timeout thread
        self.playerActive = 0    # {player_one : 0, player_two : 1}
        self.lose = (False, None, None)    # (did someone lose?, loserId, message)


    def loadConfig(self, data):
        self.playerOneTimer = int(data["player_time"])
        self.playerTwoTimer = int(data["player_time"])
        self.movsRepeated = int(data["movs_repeated"])
        self.maxMovs = int(data["max_movs"])
        self.timeout = int(data["timeout"])

    def newTurn(self, player):
        self.timeThread  = threading.Timer(self.timeout, self.playerTimeout)
        self.timeThread.start()

    def resetTimeOut(func):
        def wrapper(self, *args):
            self.timeThread.cancel()
            return func(self, *args)
        return wrapper

    def playerTimeout(self):
        message = f"Player {self.playerActive} has disconnected!"
        self.playerLose(self.playerActive, message)
        # send disconnected player (0 or 1)

    @resetTimeOut
    def receivedMovement(self, movement, elapsedTime):
        if self.playerActive == 0:
            self.playerOneTimer -= elapsedTime
            if self.playerOneTimer <= 0:
                message = f"Player {self.playerActive} ran out of time!"
                self.playerLose(self.playerActive, message)
                return
            self.playerActive = 1    
        else:
            self.playerTwoTimer -= elapsedTime
            if self.playerTwoTimer <= 0:
                message = f"Player {self.playerActive} ran out of time!"
                self.playerLose(self.playerActive, message)
                return
            self.playerActive = 0       
        self.newTurn(self.playerActive)
        # process movement

    @resetTimeOut
    def receivedExit(self):
        message = f"Player {self.playerActive} has exit the game!"
        self.playerLose(self.playerActive, message)

        # send player exit

    @resetTimeOut
    def receivedSurrender(self):
        message = f"Player {self.playerActive} has surrender!"
        self.playerLose(self.playerActive, message)
        # send player surrender

    @resetTimeOut
    def receivedLose(self):
        message = f"Checkmate!"
        self.playerLose(self.playerActive, message)

    @resetTimeOut
    def receivedTimeRanOut(self):
        message = f"Player {self.playerActive} ran out of time!"
        self.playerLose(self.playerActive, message)
        # send player ran out of time

    def playerLose(self, player, message):
        self.lose = (True, player, message)
        # send player lose
        

