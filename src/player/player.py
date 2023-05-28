import pygame

PLAYER_SPEED = 10
PLAYER_SCALE = 5


def create_player(x, y, picked_character):
    player_img = pygame.image.load(f"player/assets/characters/{picked_character}/idle/0.png")
    player_scaled_img = pygame.transform.scale(player_img,
                                               (int(player_img.get_width() * PLAYER_SCALE),
                                                int(player_img.get_height() * PLAYER_SCALE)))
    return Player(x, y, player_scaled_img)


class Player:
    def __init__(self, x, y, skin):
        self.x = x
        self.y = y
        self.skin = skin
        self.rect = self.skin.get_rect()
        self.rect.center = (x, y)

    def move(self, move):
        if move["moving_left"]:
            self.x -= PLAYER_SPEED
        if move["moving_right"]:
            self.x += PLAYER_SPEED
        if move["moving_down"]:
            self.y += PLAYER_SPEED
        if move["moving_up"]:
            self.y -= PLAYER_SPEED
        self.rect.x = self.x
        self.rect.y = self.y

    def set_xy(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def print_player(self, local_window):
        local_window.screen.blit(self.skin, self.rect)
