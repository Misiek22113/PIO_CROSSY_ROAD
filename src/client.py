import os
import socket
import sys
import threading
import pickle
import time

import pygame

from src.player.local_window_player_movement import FPS, LocalWindowPlayerMovement, SCREEN_WIDTH, SCREEN_HEIGHT
from src.player.player import create_player

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
                        "moving_down": False
                     }

    def start_client(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server_socket.connect((self.server_ip, self.server_port))
        except ConnectionRefusedError:
            self.local_window.is_running = GAME_IS_CLOSING
            print("Server is offline.")

        while self.local_window.is_running:
            self.local_window.clock.tick(FPS)
            self.local_window.draw_background()
            self.local_window.handle_events(self.move)
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
