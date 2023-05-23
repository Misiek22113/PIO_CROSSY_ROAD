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

    def move(self):
        if self.moving_left:
            self.x -= PLAYER_SPEED
        if self.moving_right:
            self.x += PLAYER_SPEED
        if self.moving_down:
            self.y += PLAYER_SPEED
        if self.moving_up:
            self.y -= PLAYER_SPEED
        self.rect.x = self.x
        self.rect.y = self.y
