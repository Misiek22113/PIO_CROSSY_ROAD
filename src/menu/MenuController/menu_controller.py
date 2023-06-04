import socket
import pygame

from src.menu.menu import Menu
from src.menu.controls.controls import Controls
from src.menu.lobby.lobby import Lobby
from src.menu.champion_select.champion_select import ChampionSelect

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BUFFER_SIZE = 4096
SERVER_IS_FULL = "NO"

pygame.mixer.init()
pygame.mixer.music.load("src/menu/utils/menu_theme_song.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.01)

class MenuController:

    def __init__(self, server_ip, server_port):
        self.menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.controls = Controls(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.lobby = Lobby(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.champion_select = ChampionSelect(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.server_ip = server_ip
        self.server_port = server_port

    def handle_main_menu_loop(self):
        actual = "menu"
        while True:
            if actual == "menu" or actual == "back":
                actual = self.menu.handle_menu_loop()
            elif actual == "controls":
                actual = self.controls.handle_controls_loop()
            elif actual == "play" or actual == "champion_select":
                if actual == "play":
                    server_socket = self.connect_to_server()

                    if not server_socket:
                        actual = "menu"
                        continue

                actual = self.champion_select.handle_champion_select_loop(server_socket)
            elif actual == "lobby":
                actual = self.lobby.handle_lobby_loop(server_socket)

    def connect_to_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            server_socket.connect((self.server_ip, self.server_port))
            connection_message = server_socket.recv(BUFFER_SIZE).decode()
        except ConnectionRefusedError:
            print("Wrong")
            return
        except ConnectionResetError:
            server_socket.close()
            print("Wrong after connection")
            return

        if connection_message == SERVER_IS_FULL:
            print("Full")
            return

        return server_socket
