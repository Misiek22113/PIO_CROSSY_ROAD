import pygame

PLAYER_SPEED = 4


class Player:
    def __init__(self, x, y, skin):
        self.x = x
        self.y = y
        self.skin = skin
        self.rect = self.skin.get_rect()
        self.rect.center = (x, y)
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
