import pickle

import pygame

from src.game_simulation.test_obstacles import TestObstacles
from src.player.local_window_player_movement import SCREEN_WIDTH
from src.player.local_window_player_movement import SCREEN_HEIGHT
from src.player.player import create_player
from src.menu.window.window import Window
from src.player.local_window_player_movement import FPS, LocalWindowPlayerMovement, SCREEN_WIDTH, SCREEN_HEIGHT

import math

SCROLL_SPEED = 2


def create_map(screen):
    return Map(screen)


class Map(Window):
    def __init__(self, width, height, player_skins):
        super().__init__("game", width, height)
        self.background_img = pygame.image.load("src/map/assets/background.png").convert()
        self.background_width = self.background_img.get_width()
        self.tiles = math.ceil(self.background_width / SCREEN_WIDTH) + 1
        self.players = [create_player(100, 200, player_skins[0]), create_player(100, 400, player_skins[1]), create_player(100, 600, player_skins[2])]
        self.scroll = 0
        self.local_window = LocalWindowPlayerMovement(SCREEN_WIDTH, SCREEN_HEIGHT, self.screen)
        self.move = self.move = {
            "moving_left": False,
            "moving_right": False,
            "moving_up": False,
            "moving_down": False
        }
        self.obstacles = TestObstacles()

    def draw_scrolling_background(self):
        self.scroll -= SCROLL_SPEED
        for i in range(0, self.tiles):
            self.screen.blit(self.background_img, (i * self.background_width + self.scroll, 0))
        if abs(self.scroll) > self.background_width:
            self.scroll = 0

    def handle_map_loop(self, server_socket):
        while True:
            self.draw_scrolling_background()
            self.local_window.handle_events(self.move)

            server_socket.sendall(pickle.dumps(self.move))
            positions, obstacles_names, obstacles_xy = pickle.loads(server_socket.recv(4096))

            for client_number, position in enumerate(positions):
                self.players[client_number].set_xy(position)

            self.obstacles.update_obstacles(obstacles_names, obstacles_xy)

            for player in self.players:
                player.print_player(self.local_window)

            self.obstacles.print_obstacles(self.local_window)
            pygame.display.update()

