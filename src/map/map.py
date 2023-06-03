import pygame
from src.player.local_window_player_movement import SCREEN_WIDTH
from src.player.local_window_player_movement import SCREEN_HEIGHT
import math

SCROLL_SPEED = 2


def create_map(screen):
    return Map(screen)


class Map:
    def __init__(self, screen):
        self.background_img = pygame.image.load("map/assets/background.png").convert()
        self.screen = screen
        self.background_width = self.background_img.get_width()
        self.tiles = math.ceil(self.background_width / SCREEN_WIDTH) + 1
        self.scroll = 0

    def draw_scrolling_background(self):
        self.scroll -= SCROLL_SPEED
        for i in range(0, self.tiles):
            self.screen.blit(self.background_img, (i * self.background_width + self.scroll, 0))
        if abs(self.scroll) > self.background_width:
            self.scroll = 0
