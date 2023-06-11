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

PLAYER_DEATH_LINE_X = -10

LEFT_MAP_EDGE = (PLAYER_WIDTH * PLAYER_SCALE) / 2
RIGHT_MAP_EDGE = SCREEN_WIDTH - (PLAYER_WIDTH * PLAYER_SCALE) / 2
BOTTOM_MAP_EDGE = SCREEN_HEIGHT - (PLAYER_HEIGHT * PLAYER_SCALE) / 2
TOP_MAP_EDGE = SCREEN_HEIGHT - SCREEN_FLOOR_HEIGHT - (PLAYER_HEIGHT * PLAYER_SCALE) / 3


FRAMES_TO_ANIMATE = 30
FRAMES_BOUNDARY_TO_START_ANIMATE = 8
FRAMES_BOUNDARY_TO_STOP_ANIMATE = 22

def create_player(x, y, picked_character):
    player_img = pygame.image.load(f"src/player/assets/characters/{picked_character}/run/0.png")
    player_scaled_img = pygame.transform.scale(player_img,
                                               (int(player_img.get_width() * PLAYER_SCALE),
                                                int(player_img.get_height() * PLAYER_SCALE)))
    player_img_animation = pygame.image.load(f"src/player/assets/characters/{picked_character}/run/1.png")
    player_scaled_img_animation = pygame.transform.scale(player_img_animation,
                                                         (int(player_img_animation.get_width() * PLAYER_SCALE),
                                                          int(player_img_animation.get_height() * PLAYER_SCALE)))
    return Player(x, y, player_scaled_img, player_scaled_img_animation, picked_character)


class Player:
    def __init__(self, x, y, skin, skin_animation, picked_character):
        self.x = x
        self.y = y
        self.pos = 1
        self.skin = skin
        self.skin_animation = skin_animation
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

    def set_position_and_status(self, position_and_status):
        self.rect.center = (position_and_status[X], position_and_status[Y])
        self.x = position_and_status[X]
        self.y = position_and_status[Y]

        if position_and_status[2] and not self.is_dead:
            self.set_dead_skin()

    def set_dead_skin(self):
        self.skin = pygame.image.load(f"src/player/assets/characters/{self.picked_character}/dead/0.png")
        self.skin = pygame.transform.scale(self.skin,
                                           (int(self.skin.get_width() * PLAYER_SCALE),
                                            int(self.skin.get_height() * PLAYER_SCALE)))
        self.skin_animation = self.skin

    def player_animation_controller(self, move, local_window):
        frame = move % FRAMES_TO_ANIMATE
        if frame < FRAMES_BOUNDARY_TO_START_ANIMATE or frame > FRAMES_BOUNDARY_TO_STOP_ANIMATE:
            local_window.screen.blit(self.skin, self.rect)
        elif FRAMES_BOUNDARY_TO_START_ANIMATE <= frame <= FRAMES_BOUNDARY_TO_STOP_ANIMATE:
            local_window.screen.blit(self.skin_animation, self.rect)

    def print_player(self, local_window):
        self.player_animation_controller(self.pos, local_window)
        self.pos += 1
        if self.pos == FRAMES_TO_ANIMATE:
            self.pos = 0

    def handle_screen_edges(self, move):
        if self.rect.center[X] >= RIGHT_MAP_EDGE:
            move["moving_right"] = False
        elif self.rect.center[X] <= LEFT_MAP_EDGE:
            move["moving_left"] = False

        if self.rect.center[Y] >= BOTTOM_MAP_EDGE:
            move["moving_down"] = False
        elif self.rect.center[Y] <= TOP_MAP_EDGE:
            move["moving_up"] = False

        if self.rect.center[X] <= PLAYER_DEATH_LINE_X:
            self.is_dead = True
            move["has_died"] = True
