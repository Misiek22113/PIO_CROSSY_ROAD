import os
import socket
import sys
import threading
import pickle
from typing import NoReturn

from game import Game
HOST_IP = "127.0.0.1"
HOST_PORT = 6000

SIZE_OF_CONNECT_MESSAGE = 35
SIZE_OF_POSITIONS_LIST = 88

EXIT = 0


class Client:
    def __init__(self, server_ip: str, server_port: int) -> NoReturn:
        self.server_ip = server_ip
        self.server_port = server_port
        self.map = Game()
        self.server_socket = None

    def start_connection(self) -> NoReturn:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((self.server_ip, self.server_port))
        message = self.server_socket.recv(SIZE_OF_CONNECT_MESSAGE).decode()
        if message == 'NO':
            self.server_socket.close()
            sys.exit(EXIT)

    def start_game(self) -> NoReturn:
        threading.Thread(target=self.get_move).start()
        threading.Thread(target=self.get_map).start()

    def get_map(self) -> NoReturn:
        while True:
            positions = pickle.loads(self.server_socket.recv(SIZE_OF_POSITIONS_LIST))

            for player_number, position in enumerate(positions):
                self.map.actual_position(position, player_number)

            os.system('cls')
            print(self.map)
            print('Move: ')

    def get_move(self) -> NoReturn:
        while True:
            move = input()
            self.server_socket.sendall(move.encode())


client = Client(HOST_IP, HOST_PORT)
client.start_connection()
client.start_game()
