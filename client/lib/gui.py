import logging
import pygame
import os, sys

sys.path.append(os.path.join(sys.path[0], 'lib', 'screens'))
sys.path.append(os.path.join(sys.path[0], 'lib', 'screens', 'utils'))

from titleScreen import TitleScreen


class GUI:

    def __init__(self, networkManager):
        pygame.init()
        self.width = None
        self.height = None
        self.title = None
        self.icon = None    # image path
        self.logo = None    # image path
        self.backgroundColor = None
        self.screen = None
        self.titleScreen = None    # home screen (name and room selection)
        self.networkManager = networkManager

    def __repr__(self):
        return f'GUI(width: {self.width!r}, height: {self.height!r}, icon: {self.icon!r}\
        , logo: {self.logo!r}, backgroundColor: {self.background})'

    def __str__(self):
        return f'GUI - width: {self.width!r}, height: {self.height!r}'

    def loadConfig(self, data):
        self.width = data["width"]
        self.height = data["height"]
        self.title = data["title"]
        self.icon = data["icon"]
        self.logo = data["logo"]
        red, green, blue = data["background"].split(',')
        self.backgroundColor = (int(red), int(green), int(blue))

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

        icon = pygame.image.load(self.icon)
        pygame.display.set_icon(icon)

        logo = pygame.image.load(self.logo)

        self.titleScreen = TitleScreen(screen=self.screen, bg=self.backgroundColor, logo=logo, networkManager=self.networkManager)

        logging.debug(f"GUI created.")

    def showScreen(self, events):
        self.screen = self.titleScreen.getScreen(events)
        

        