import pygame
from pygame.locals import *

class Menu:

    screen = {}
    BACKGROUND_IMAGE = pygame.image.load("menu/menu_background.svg")

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def createWindowMenu(self):
        pygame.display.set_caption('Menu')
        screen_size = (self.width, self.height)
        self.screen = pygame.display.set_mode(screen_size)

    def printWindowMenu(self):
        self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))