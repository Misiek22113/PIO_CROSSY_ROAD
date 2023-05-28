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

QUIT = "q"
CLOSE_SIGNAL = None
CLOSE_SIGNAL_ERROR = False

SERVER_IS_NOT_CONNECT = None

CLIENT_IS_RUNNING = False
CLIENT_IS_CLOSING = True

HOST_IP = "127.0.0.1"
HOST_PORT = 6000

SIZE_OF_CONNECT_MESSAGE = 40
SIZE_OF_RECV_WITH_POSITIONS = 1000

DISCONNECT_MESSAGE = "NO"
CLOSING_MESSAGE = b"c"


class Client:

    def __init__(self):
        self.server_ip = HOST_IP
        self.server_port = HOST_PORT
        self.server_socket = SERVER_IS_NOT_CONNECT
        self.client_status = CLIENT_IS_RUNNING
        self.map = Game()
        pygame.init()
        self.local_window = LocalWindowPlayerMovement(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player = create_player(100, 100, "spiderman")
        self.move = {
                    "moving_left": False,
                    "moving_right": False,
                    "moving_up": False,
                    "moving_down": False
                     }
        self.lock = threading.Lock()

    def start_client(self):
        threading.Thread(target=self.start_connection).start()

        while self.local_window.is_running:
            self.local_window.clock.tick(FPS)
            self.local_window.draw_background()
            self.local_window.handle_events(self.move)

            # self.player.move(self.move)
            self.player.print_player(self.local_window)

            pygame.display.update()

        pygame.quit()

    def start_connection(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.server_socket.connect((self.server_ip, self.server_port))
        except ConnectionRefusedError:
            print("Server is offline.")
            sys.exit()

        connection_message = self.server_socket.recv(SIZE_OF_CONNECT_MESSAGE).decode()

        if connection_message == DISCONNECT_MESSAGE:
            print("Server is full.")
            self.server_socket.close()
            sys.exit()

        threading.Thread(target=self.start_game).start()

    def start_game(self):
        threading.Thread(target=self.receive_move).start()

    def receive_move(self):
        while True:
            tak = time.time()
            positions = pickle.loads(self.server_socket.recv(SIZE_OF_RECV_WITH_POSITIONS))
            self.server_socket.sendall(pickle.dumps(self.move))
            self.player.set_xy(positions[0], positions[1])
            print(tak - time.time())

# TODO delete later
client = Client()
client.start_client()
