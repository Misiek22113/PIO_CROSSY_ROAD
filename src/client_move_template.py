import socket
import pickle
import map.map

import pygame

from src.player.local_window_player_movement import FPS, LocalWindowPlayerMovement, SCREEN_WIDTH, SCREEN_HEIGHT
from src.player.player import create_player
from src.game_simulation.test_obstacles import TestObstacles

SERVER_QUIT = 2
CLIENT_QUIT = 1

GAME_IS_CLOSING = False
PLACE_FOR_SOCKET = None

PLAYER_POSITION_Y = 100
PLAYER_POSITION_X = 100

HOST_IP = "127.0.0.1"
HOST_PORT = 6000

SIZE_OF_RECV_WITH_POSITIONS = 1000


class Client:

    def __init__(self):
        self.server_ip = HOST_IP
        self.server_port = HOST_PORT
        self.server_socket = PLACE_FOR_SOCKET
        pygame.init()
        self.local_window = LocalWindowPlayerMovement(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player = create_player(PLAYER_POSITION_X, PLAYER_POSITION_Y, "spiderman")
        self.move = {
                        "quit": False,
                        "moving_left": False,
                        "moving_right": False,
                        "moving_up": False,
                        "moving_down": False,
                        "is_colliding": False
                     }
        self.map = map.map.create_map(self.local_window.screen)

    def start_client(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server_socket.connect((self.server_ip, self.server_port))
        except ConnectionRefusedError:
            self.local_window.is_running = GAME_IS_CLOSING
            print("Server is offline.")

        test_obstacle = TestObstacles()
        test_obstacle.add_obstacle()

        while self.local_window.is_running:
            self.local_window.clock.tick(FPS)
            self.map.draw_scrolling_background()
            self.local_window.handle_events(self.move)
            test_obstacle.handle_obstacles(self.local_window.screen)

            for obstacle in test_obstacle.obstacles:
                if self.player.rect.colliderect(obstacle.rect):
                    self.move["is_colliding"] = True
                    break
                else:
                    self.move["is_colliding"] = False

            try:
                self.server_socket.sendall(pickle.dumps(self.move))
                positions = pickle.loads(self.server_socket.recv(SIZE_OF_RECV_WITH_POSITIONS))
            except ConnectionResetError:
                self.local_window.is_running = GAME_IS_CLOSING
                continue

            if positions in [CLIENT_QUIT, SERVER_QUIT]:
                self.local_window.is_running = GAME_IS_CLOSING
                self.server_socket.close()
                continue

            self.player.set_xy(positions)
            self.player.print_player(self.local_window)
            pygame.display.update()

        pygame.quit()


# TODO delete later
client = Client()
client.start_client()
