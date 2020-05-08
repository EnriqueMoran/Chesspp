import pygame
import os, sys
import logging
from functools import partial

sys.path.append(os.path.join(sys.path[0], 'utils'))

from screen import Screen
from button import Button
from pygame_textinput import TextInput

class TitleScreen(Screen):

    def __init__(self, logo, networkManager, *args, **kwargs):
        super(TitleScreen, self).__init__(*args, **kwargs)
        self.logo = logo    # image object
        self.nameInput = TextInput(max_string_length=10)
        self.roomInput = TextInput(max_string_length=10)
        self.activeForm = self.nameInput    # default active form is nameInput
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.nameInputLabbel = self.font.render('Username: ', True, (0, 0, 0))
        self.roomInputLabbel = self.font.render('Room: ', True, (0, 0, 0))
        self.networkManager = networkManager

    def addLogo(self):
        width, height = self.screen.get_size()
        x = (width // 2) - (self.logo.get_size()[0] // 2)
        y = (height // 5) - (self.logo.get_size()[1] // 2)
        self.screen.blit(self.logo, (x, y))

    def enableForm(self, form):
        self.activeForm = form
        self.activeForm.cursor_visible = True
        if form == self.nameInput:
            self.roomInput.cursor_visible = False    # not working as expected
        else:
            self.nameInput.cursor_visible = False

    def addNameInput(self, x, y, events):        
        form = Button(x - 10, y - 12, 150, 50, (0, 0, 0), fill=False)
        form.action = partial(self.enableForm, form=self.nameInput)
        form.update(events)
        form.draw(self.screen)
        self.screen.blit(self.nameInput.get_surface(), (x, y))
        self.screen.blit(self.nameInputLabbel, (x - 150, y))

    def addRoomInput(self, x, y, events):        
        form = Button(x - 10, y - 12, 150, 50, (0, 0, 0), fill=False)
        form.action = partial(self.enableForm, form=self.roomInput)
        form.update(events)
        form.draw(self.screen)
        self.screen.blit(self.roomInput.get_surface(), (x, y))
        self.screen.blit(self.roomInputLabbel, (x - 100, y))

    def enterRoom(self, playerName, roomId):
        # check if can reach server
        print(f"Player {playerName} entering room {roomId}...")
        message = f"0::{roomId}${playerName}-127.0.0.1"    # add player to room TODO: get real IP
        self.networkManager.sendMessage(message)
        logging.debug(f"Player {playerName} entering room {roomId}...")
        logging.debug(f"Mesage sent: {message}")

    def addJoinRoomButton(self, events):
        width, height = self.screen.get_size()
        x = (width // 2) - (140 // 2)
        y = (height // 6 * 5) - (40 // 2)
        button = Button(x, y, 140, 40, (227, 218, 209), text="Join room")
        button.action = partial(self.enterRoom, playerName=self.nameInput.get_text(), roomId=self.roomInput.get_text())
        button.update(events)
        button.draw(self.screen)

    def getScreen(self, events):
        self.addBackgroundColor()
        self.addLogo()
        self.addNameInput(200, 300, events)
        self.addRoomInput(200, 400, events)
        self.addJoinRoomButton(events)
        self.activeForm.update(events)
        return self.screen