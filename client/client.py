import logging
import socket
import random
import pygame
import os, sys
import time

sys.path.append(os.path.join(sys.path[0], 'lib'))

from fileInput import FileReader
from gui import GUI
from networkManager import NetworkManager

networkManager = None

def loadCfg():
    filePaths = [
        "config/main.cfg",
        "config/pieces.cfg"
    ]
    return FileReader(filePaths)

def createLog(data):
    debugLog = data["debug_log"]
    if os.path.exists(debugLog): os.remove(debugLog)    # delete log file
    logging.basicConfig(filename=debugLog, level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')

def run():
    global networkManager

    fileReader = loadCfg()    # create fileReader object
    fileReader.loadConfigFiles()
    fileReader.loadMain()
    createLog(fileReader.log_data)

    networkManager = NetworkManager()
    networkManager.loadConfig(fileReader.networkManager_data)
    print("Network Manager started.")

    gui = GUI()
    gui.loadConfig(fileReader.screen_data)
    clock = pygame.time.Clock()

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                # TODO: call closing methods/classes
                running = False

        gui.showScreen(events)
        
        pygame.display.update()
        clock.tick(30)



def test():
    messages = [
    "addPlayer(1234, Oviejo)",
    "addPlayer(1234, El6pesetas)",
    "addPlayer(1234, Beyenes)",
    "addPlayer(1234, Moyen)",
    "sendMovement(1234, movement)",
    "sendMovement(1234, movement)",
    "sendMovement(1234, movement)",
    "addPlayer(7890, moyen)",
    "addPlayer(7890, beyenes)",
    "sendMovement(1234, movement)",
    "sendMovement(1234, movement)",
    "sendMovement(7890, movement)",
    "sendMovement(1234, movement)",
    "sendMovement(7890, movement)",
    "sendMovement(7890, movement)",
    "sendMovement(7890, movement)",
    "sendMovement(1234, movement)",
    "sendExit(1234)",
    "addPlayer(8412, Ryannerex)",
    "addPlayer(9301, Storm)",
    "sendMovement(7890, movement)",
    "sendMovement(7890, movement)",
    "sendMovement(7890, movement)",
    "sendMovement(7890, movement)",
    "sendLose(7890)",
    "addPlayer(9301, Imp)",
    "sendMovement(9301, movement)",
    "sendMovement(9301, movement)",
    "addPlayer(8412, Gerwin)",
    "sendMovement(8412, movement)",
    "sendMovement(9301, movement)",
    "sendMovement(8412, movement)",
    "sendSurrender(8412)",
    "addPlayer(2888, Merlin)",
    "sendMovement(9301, movement)",
    "sendMovement(9301, movement)",
    "addPlayer(2888, Foamer)",
    "sendMovement(2888, movement)",
    "sendMovement(2888, movement)",
    "sendTimeOut(9301)",
    "sendMovement(2888, movement)",
    "sendExit(2888)"
    ]
    for message in messages:
        sendMsg(message)
        time.sleep(random.uniform(0.001, 0.1))

def test():

    print("Available commands:\n\
        - addPlayer(roomId, playerName)\n\
        - sendMovement(roomId, movement)\n\
        - sendExit(roomId)\n\
        - sendSurrender(roomId)\n\
        - sendLose(roomId)\n\
        - sendTimeOut(roomId)\n\
        - test()\n")
    while True:
        message = input()
        sendMsg(message)

def sendMsg(message):
    command = message.split('(')[0]
    parameters = message.split('(')[1].split(')')[0]
    try:
        roomId = int(parameters.split(',')[0])
    except:
        pass
    msg = ""
    if command == "addPlayer":    # add player 1
        name = parameters.split(',')[1].strip()
        msg = f"0::{roomId}${name}-127.0.0.1"
    elif command == "sendMovement":
        movement = parameters.split(',')[1]
        msg = f"1::{roomId}$1-{movement}, 10"
    elif command == "sendExit":
        msg = f"1::{roomId}$2"
    elif command == "sendSurrender":
        msg = f"1::{roomId}$3"
    elif command == "sendLose":
        msg = f"1::{roomId}$4"
    elif command == "sendTimeOut":
        msg = f"1::{roomId}$5"
    elif command == "test":
        test()
    s.sendall(bytes(msg, "utf-8"))
    if msg:
        print(f"sent message: {msg}\n")



if __name__ == "__main__":
    run()
    pygame.quit()