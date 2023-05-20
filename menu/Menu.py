import pygame
from pygame.locals import *

pygame.font.init()

class Menu:

    screen = {}
    BACKGROUND_IMAGE = pygame.image.load("menu/menu_background.svg")
    TEXT_COLOR = (255, 255, 255)
    FONT_HEADER = pygame.font.Font("menu/PressStart2P-Regular.ttf", 100)
    FONT_OPTION = pygame.font.Font("menu/PressStart2P-Regular.ttf", 60)

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw_text(self, text, x, y, font):
        img = font.render(text, True, self.TEXT_COLOR)
        img_rect = img.get_rect(center=(x, y))
        self.screen.blit(img, img_rect)
 
    def create_window_menu(self):
        pygame.display.set_caption('Menu')
        screen_size = (self.width, self.height)
        self.screen = pygame.display.set_mode(screen_size)

    def print_window_menu(self):
        self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))
        self.draw_text("MAIN MENU", 640, 100, self.FONT_HEADER)
        self.draw_text("PLAY", 640, 250, self.FONT_OPTION)
        self.draw_text("NAVIGATING", 640, 350, self.FONT_OPTION)
        self.draw_text("EXIT", 640, 450, self.FONT_OPTION)

    def 