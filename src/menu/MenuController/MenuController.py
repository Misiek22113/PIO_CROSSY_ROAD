import socket

from src.menu.Menu import Menu
from src.menu.controls.Controls import Controls
from src.menu.lobby.Lobby import Lobby
from src.menu.champion_select.champion_select import ChampionSelect

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class MenuController:

    def __init__(self):
        self.menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.controls = Controls(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.lobby = Lobby(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.champion_select = ChampionSelect(SCREEN_WIDTH, SCREEN_HEIGHT)

    def handle_main_menu_loop(self, connection_detail):
        actual = "menu"
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            if actual == "menu" or actual == "back" or actual == "closed_socket":
                actual = self.menu.handle_menu_loop()
            elif actual == "controls":
                actual = self.controls.handle_controls_loop()
            elif actual == "play" or actual == "champion_select":
                if actual == "play":
                    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        server_socket.connect(connection_detail)
                    except ConnectionRefusedError:
                        print("Wrong")
                        actual = "menu"
                        continue

                    try:
                        connection_message = server_socket.recv(124).decode()
                    except ConnectionResetError:
                        server_socket.close()
                        print("Wrong")
                        actual = "menu"
                        continue

                    if connection_message == "NO":
                        print("Full")
                        actual = "menu"
                        continue

                actual = self.champion_select.handle_champion_select_loop(server_socket)
            elif actual == "lobby":
                actual = self.lobby.handle_lobby_loop(server_socket)
