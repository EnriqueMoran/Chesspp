import logging
import signal
import os, sys
import time

sys.path.append(os.path.join(sys.path[0], 'lib'))

from fileInput import FileReader
from player import Player
from room import Room
from roomManager import RoomManager
from networkManager import NetworkManager


networkManager = None
roomManager = None

def loadCfg():
    filePaths = [
        "config/main.cfg",
        "config/pieces.cfg",
        "config/database.cfg"
    ]
    return FileReader(filePaths)


def createLog(data):
    debugLog = data["debug_log"]
    if os.path.exists(debugLog): os.remove(debugLog)    # delete log file
    logging.basicConfig(filename=debugLog, level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')
  

def exitHandler(signal, frame):
    logging.info("Ctrl + C pressed, closing server...")
    print("Ctrl + C pressed, closing server...")
    # save game status, db, etc
    logging.info("Server closed")
    print("Server closed")
    try:
        os._exit(1)    # this is dangerous!!
    except Exception as e:
        print(e)

def run():
    global networkManager, roomManager

    print("Starting server...")
    fileReader = loadCfg()    # create fileReader object
    fileReader.loadConfigFiles()
    fileReader.loadMain()

    createLog(fileReader.log_data)

    networkManager = NetworkManager()
    networkManager.loadConfig(fileReader.networkManager_data)
    print("Network Manager started.")

    roomManager = RoomManager(fileReader.board_data, fileReader.turn_data, fileReader.messageType_data)
    roomManager.loadConfig(fileReader.roomManager_data)
    print("Room Manager started.")

    signal.signal(signal.SIGINT, exitHandler)
    print("Server runnig!")


def test():
    while True:
        try:
            data = networkManager.getMessage()
            if data:
                message, socket = data
                response = roomManager.receivedMessage(message)
                time.sleep(0.05)    # simulates processing time
                networkManager.processResponse(response, socket)
            else:
               pass
        except Exception as e:
            logging.critical(f"Server closing. Error: {e!s}")
            break


if __name__ == "__main__":
    run()
    test()

