import json

class FileReader:

    def __init__(self, configFiles):
        self._configFiles = configFiles    # all config files paths
        self.main_configFile = ""
        self.pieces_configFile = ""
        self.database_configFile = ""

        # config data (raw)
        self.player_data = ""
        self.board_data = ""
        self.database_data = ""
        self.log_data = ""
        self.turn_data = ""
        self.roomManager_data = ""
        self.messageType_data = ""
        self.networkManager_data = ""

    def loadConfigFiles(self):
        for filePath in self._configFiles:
            fileName = filePath.split('/')[::-1][0]
            self.__setFilePath(fileName, filePath)

    def __setFilePath(self, fileName, filePath):
        if fileName == "main.cfg":
            self.main_configFile = filePath
        elif fileName == "pieces.cfg":
            self.pieces_configFile = filePath
        elif fileName == "database.cfg":
            self.database_configFile = filePath

    def loadMain(self):
        with open(self.main_configFile) as file:
            data = json.load(file)
            self.player_data = data["player"]
            self.board_data = data["board"]
            self.log_data = data["log"]
            self.turn_data = data["turn"]
            self.roomManager_data = data["roomManager"]
            self.messageType_data = data["messageType"]
            self.networkManager_data = data["networkManager"]

    def loadPieces(self):
        with open(self.pieces_configFile) as file:
            data = json.load(file)

    def loadDatabase(self):
        with open(self.database_configFile) as file:
            data = json.load(file)
            self.database_data = data["database"]