import json


class FileReader:

    def __init__(self, configFiles):
        self._configFiles = configFiles    # all config files paths
        self.main_configFile = ""

        # config data (raw)
        self.log_data = ""
        self.networkManager_data = ""
        self.screen_data = ""
        self.images_data = ""

    def loadConfigFiles(self):
        for filePath in self._configFiles:
            fileName = filePath.split('/')[::-1][0]
            self.__setFilePath(fileName, filePath)

    def __setFilePath(self, fileName, filePath):
        if fileName == "main.cfg":
            self.main_configFile = filePath

    def loadMain(self):
        with open(self.main_configFile) as file:
            data = json.load(file)
            self.log_data = data["log"]
            self.networkManager_data = data["networkManager"]
            self.screen_data = data["screen"]
            self.images_data = data["images"]

    def loadPieces(self):
        with open(self.pieces_configFile) as file:
            data = json.load(file)
