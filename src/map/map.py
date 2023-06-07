import pickle
import sys

import pygame

from src.game_simulation.test_obstacles import TestObstacles
from src.player.player import create_player
from src.menu.window.window import Window
from src.player.local_window_player_movement import LocalWindowPlayerMovement, SCREEN_WIDTH, SCREEN_HEIGHT

import math

BUFFER_SIZE = 4096

LOST = 9
WIN = 10

EMPTY_OBSTACLES = None

INIT_SCROLL = 0
SCROLL_SPEED = 3

FIRST_PLAYER_POSITION = [100, 200]
SECOND_PLAYER_POSITION = [100, 400]
THIRD_PLAYER_POSITION = [100, 600]

FIRST_PLAYER = 0
SECOND_PLAYER = 1
THIRD_PLAYER = 2


class Map(Window):
    def __init__(self, width, height, player_skins):
        super().__init__("game", width, height)
        self.background_img = pygame.image.load("src/map/assets/background.png").convert()
        self.background_width = self.background_img.get_width()
        self.tiles = math.ceil(self.background_width / SCREEN_WIDTH) + 1
        self.players = [create_player(*FIRST_PLAYER_POSITION, player_skins[FIRST_PLAYER]),
                        create_player(*SECOND_PLAYER_POSITION, player_skins[SECOND_PLAYER]),
                        create_player(*THIRD_PLAYER_POSITION, player_skins[THIRD_PLAYER])]
        self.scroll = INIT_SCROLL
        self.local_window = LocalWindowPlayerMovement(SCREEN_WIDTH, SCREEN_HEIGHT, self.screen)
        self.move = {
            "quit": False,
            "moving_left": False,
            "moving_right": False,
            "moving_up": False,
            "moving_down": False,
            "is_colliding_with_pushing": False,
            "is_colliding": False,
            "has_won": False
        }
        self.obstacles = EMPTY_OBSTACLES

    def draw_scrolling_background(self):
        self.scroll -= SCROLL_SPEED
        for i in range(0, self.tiles):
            self.screen.blit(self.background_img, (i * self.background_width + self.scroll, 0))
        if abs(self.scroll) > self.background_width:
            self.scroll = 0

    def handle_map_loop(self, server_socket):
        self.obstacles = TestObstacles()
        try:
            while True:
                self.draw_scrolling_background()
                self.local_window.handle_events(self.move)
                server_socket.sendall(pickle.dumps(self.move))

                if self.move["quit"]:
                    server_socket.close()
                    pygame.quit()
                    sys.exit()

                positions, obstacles_names, obstacles_xy = pickle.loads(server_socket.recv(BUFFER_SIZE))

                if isinstance(positions, int):
                    server_socket.close()
                    if positions == WIN:
                        return "win", obstacles_xy
                    elif positions == LOST:
                        return "lost", obstacles_xy
                    else:
                        return "server_is_closed", None

                for client_number, position in enumerate(positions):
                    self.players[client_number].set_xy(position)

                self.obstacles.update_obstacles(obstacles_names, obstacles_xy)

                for player in self.players:
                    player.print_player(self.local_window)

                self.obstacles.print_obstacles(self.local_window)
                pygame.display.update()
        except (ConnectionResetError, ConnectionAbortedError):
            return "lost_connection_with_server", None

