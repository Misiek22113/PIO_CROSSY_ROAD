import pygame
from src.menu.MenuController.menu_controller import MenuController

HOST_IP = "127.0.0.1"
HOST_PORT = 6001


class Client:

    def __init__(self):
        self.server_ip = HOST_IP
        self.server_port = HOST_PORT
        pygame.display.init()

    def start_game(self):
        menu = MenuController(self.server_ip, self.server_port)
        menu.handle_main_menu_loop()


client = Client()
client.start_game()
