import socket
import pickle

import pygame

from src.menu.MenuController.MenuController import MenuController
from src.player.local_window_player_movement import FPS, LocalWindowPlayerMovement, SCREEN_WIDTH, SCREEN_HEIGHT
from src.player.player import create_player

SERVER_QUIT = 2
CLIENT_QUIT = 1

GAME_IS_CLOSING = False
PLACE_FOR_SOCKET = None

PLAYER_POSITION_Y = 100
PLAYER_POSITION_X = 100

HOST_IP = "127.0.0.1"
HOST_PORT = 6001

SIZE_OF_RECV_WITH_POSITIONS = 1000


class Client:

    def __init__(self):
        self.server_ip = HOST_IP
        self.server_port = HOST_PORT
        self.server_socket = PLACE_FOR_SOCKET
        pygame.display.init()
        self.local_window = LocalWindowPlayerMovement(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.move = {
                        "quit": False,
                        "moving_left": False,
                        "moving_right": False,
                        "moving_up": False,
                        "moving_down": False
                     }

    def start_game(self):
        menu = MenuController()
        menu.handle_main_menu_loop((self.server_ip, self.server_port))

client = Client()
client.start_game()