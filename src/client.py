import os
import socket
import sys
import threading
import pickle
import time

import pygame

from game_simulation.game import Game
from src.player.local_window_player_movement import FPS, LocalWindowPlayerMovement, SCREEN_WIDTH, SCREEN_HEIGHT
from src.player.player import create_player

HOST_IP = "127.0.0.1"
HOST_PORT = 6000

SIZE_OF_RECV_WITH_POSITIONS = 1000


class Client:

    def __init__(self):
        self.server_ip = HOST_IP
        self.server_port = HOST_PORT
        self.server_socket = None
        pygame.init()
        self.local_window = LocalWindowPlayerMovement(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player = create_player(100, 100, "spiderman")
        self.move = {
                    "moving_left": False,
                    "moving_right": False,
                    "moving_up": False,
                    "moving_down": False
                     }

    def start_client(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((self.server_ip, self.server_port))
        while self.local_window.is_running:
            self.local_window.clock.tick(FPS)
            self.local_window.draw_background()
            self.local_window.handle_events(self.move)

            positions = pickle.loads(self.server_socket.recv(SIZE_OF_RECV_WITH_POSITIONS))
            self.server_socket.sendall(pickle.dumps(self.move))
            self.player.set_xy(positions[0], positions[1])
            self.player.print_player(self.local_window)

            pygame.display.update()

        pygame.quit()

# TODO delete later
client = Client()
client.start_client()
