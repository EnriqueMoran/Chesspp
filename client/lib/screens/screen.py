import pygame

class Screen:

    def __init__(self, screen, bg):
        self.screen = screen
        self.backgroundColor = bg

    def addBackgroundColor(self):
        self.screen.fill(self.backgroundColor)
