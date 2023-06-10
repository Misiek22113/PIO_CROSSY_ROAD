import pygame
from src.player.local_window_player_movement import SCREEN_WIDTH
from src.player.local_window_player_movement import SCREEN_HEIGHT
from src.player.local_window_player_movement import SCREEN_FLOOR_HEIGHT

Y = 1
X = 0

PLAYER_SPEED = 10
PLAYER_SCALE = 5
SCROLL_SPEED = 3

PLAYER_WIDTH = 14
PLAYER_HEIGHT = 20


def create_player(x, y, picked_character):
    player_img = pygame.image.load(f"src/player/assets/characters/{picked_character}/idle/0.png")
    player_scaled_img = pygame.transform.scale(player_img,
                                               (int(player_img.get_width() * PLAYER_SCALE),
                                                int(player_img.get_height() * PLAYER_SCALE)))
    return Player(x, y, player_scaled_img, picked_character)


class Player:
    def __init__(self, x, y, skin, picked_character):
        self.x = x
        self.y = y
        self.skin = skin
        self.rect = self.skin.get_rect()
        self.rect.center = (x, y)
        self.is_dead = False
        self.picked_character = picked_character

    def move(self, move):
        if move["has_died"]:
            self.is_dead = True

        if self.is_dead:
            move["moving_left"] = False
            move["moving_right"] = False
            move["moving_up"] = False
            move["moving_down"] = False

        if move["is_colliding_with_pushing"]:
            self.x -= SCROLL_SPEED

        self.handle_screen_edges(move)

        if move["has_won"]:
            self.rect.center = (self.x, self.y)
            return

        if move["moving_left"]:
            self.x -= PLAYER_SPEED
        if move["moving_right"]:
            self.x += PLAYER_SPEED
        if move["moving_down"]:
            self.y += PLAYER_SPEED
        if move["moving_up"]:
            self.y -= PLAYER_SPEED

        self.rect.center = (self.x, self.y)

    def set_xy(self, xy):
        self.rect.center = (xy[X], xy[Y])

    def print_player(self, local_window):
        local_window.screen.blit(self.skin, self.rect)

    def handle_screen_edges(self, move):
        if self.rect.center[X] >= SCREEN_WIDTH - (PLAYER_WIDTH * PLAYER_SCALE) / 2:
            move["moving_right"] = False
        elif self.rect.center[X] <= (PLAYER_WIDTH * PLAYER_SCALE) / 2:
            move["moving_left"] = False

        if self.rect.center[Y] >= SCREEN_HEIGHT - (PLAYER_HEIGHT * PLAYER_SCALE) / 2:
            move["moving_down"] = False
        elif self.rect.center[Y] <= SCREEN_HEIGHT - SCREEN_FLOOR_HEIGHT - (PLAYER_HEIGHT * PLAYER_SCALE) / 3:
            move["moving_up"] = False
