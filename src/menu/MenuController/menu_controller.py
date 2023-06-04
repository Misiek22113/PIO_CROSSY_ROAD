import socket
import pygame

from src.map.map import Map
from src.menu.end_game_result.end_game_result import EndGameResult
from src.menu.menu import Menu
from src.menu.controls.controls import Controls
from src.menu.lobby.lobby import Lobby
from src.menu.champion_select.champion_select import ChampionSelect
from src.menu.notification.Notification import Notification

EMPTY_MAP = None
WIN = True
LOST = False

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
        self.server_offline_notification = Notification(
            SCREEN_WIDTH, SCREEN_HEIGHT, "server_offline", "Server is offline.", "menu")
        self.lost_connection_with_server = Notification(
            SCREEN_WIDTH, SCREEN_HEIGHT, "lost_connection", "Connection with server is lost.", "menu")
        self.server_is_full = Notification(
            SCREEN_WIDTH, SCREEN_HEIGHT, "server_is_full", "Server is full.", "menu")
        self.server_is_closed = Notification(
            SCREEN_WIDTH, SCREEN_HEIGHT, "server_is_closed", "Server is closed.", "menu")
        self.champion_is_picked = Notification(
            SCREEN_WIDTH, SCREEN_HEIGHT, "champion_is_picked", "Champion is picked already.", "champion_select")
        self.map = EMPTY_MAP
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

                    if isinstance(server_socket, str):
                        actual = server_socket
                        continue

                actual = self.champion_select.handle_champion_select_loop(server_socket)
            elif actual == "lobby":
                actual, players = self.lobby.handle_lobby_loop(server_socket)
            elif actual == "server_offline_notification":
                actual = self.server_offline_notification.handle_notification_loop()
            elif actual == "lost_connection_with_server":
                actual = self.lost_connection_with_server.handle_notification_loop()
            elif actual == "server_is_full":
                actual = self.lost_connection_with_server.handle_notification_loop()
            elif actual == "server_is_closed":
                actual = self.server_is_closed.handle_notification_loop()
            elif actual == "champion_is_picked":
                actual = self.champion_is_picked.handle_notification_loop()
            elif actual == "game":
                self.map = Map(SCREEN_WIDTH, SCREEN_HEIGHT, players)
                actual, champion = self.map.handle_map_loop(server_socket)
            elif actual == "lost":
                actual = EndGameResult("lost", champion, LOST).handle_end_game_result_loop()
            elif actual == "win":
                actual = EndGameResult("win", champion, WIN).handle_end_game_result_loop()

    def connect_to_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            server_socket.connect((self.server_ip, self.server_port))
            connection_message = server_socket.recv(BUFFER_SIZE).decode()
        except ConnectionRefusedError:
            return "server_offline_notification"
        except ConnectionResetError:
            server_socket.close()
            return "lost_connection_with_server"

        if connection_message == SERVER_IS_FULL:
            return "server_is_full"

        return server_socket
