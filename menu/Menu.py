import pygame
from pygame.locals import *

from menu.button.Button import Button

pygame.font.init()


class Menu:
    screen = {}
    PLAY_BUTTON = {}
    NAVIGATION_BUTTON = {}
    QUIT_BUTTON = {}
    BACKGROUND_IMAGE = pygame.image.load("menu/menu_background.svg")
    TEXT_COLOR = (255, 255, 255)
    BASE_COLOR = (249, 154, 40)
    HOVERING_COLOR = (230, 205, 87)
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
        self.PLAY_BUTTON = Button(None, pos=(640, 250), text_input="PLAY", font=self.FONT_OPTION,
                                  base_color=self.BASE_COLOR, hovering_color=self.HOVERING_COLOR)
        self.NAVIGATION_BUTTON = Button(None, pos=(640, 350), text_input="NAVIGATING", font=self.FONT_OPTION,
                                        base_color=self.BASE_COLOR, hovering_color=self.HOVERING_COLOR)
        self.QUIT_BUTTON = Button(None, pos=(640, 450), text_input="QUIT", font=self.FONT_OPTION,
                                  base_color=self.BASE_COLOR, hovering_color=self.HOVERING_COLOR)

    def handle_menu_loop(self):
        for button in [self.PLAY_BUTTON, self.NAVIGATION_BUTTON, self.QUIT_BUTTON]:
            button.change_color(pygame.mouse.get_pos())
            button.update(self.screen)
