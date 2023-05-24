import os
import socket
import sys
import threading
import pickle
from io import StringIO

from game_simulation.game import Game

HOST_IP = "127.0.0.1"
HOST_PORT = 6000

SIZE_OF_CONNECT_MESSAGE = 40
SIZE_OF_RECV_WITH_POSITIONS = 2000

DISCONNECT_MESSAGE = "NO"
EXIT = 0


class Client:

    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.map = Game()
        self.server_socket = None
        self.close = False

    def start_connection(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((self.server_ip, self.server_port))
        message = self.server_socket.recv(SIZE_OF_CONNECT_MESSAGE).decode()
        print("leggo")
        if message == DISCONNECT_MESSAGE:
            self.server_socket.close()
            sys.exit(EXIT)

    def start_game(self):
        threading.Thread(target=self.get_move).start()
        threading.Thread(target=self.get_map).start()

    def get_map(self):
        while True:
            if self.close:
                self.server_socket.close()
                sys.exit()

            positions = pickle.loads(self.server_socket.recv(SIZE_OF_RECV_WITH_POSITIONS))

            if positions is None:
                self.server_socket.sendall(b"c")
                self.close = True
                self.server_socket.close()
                print("Server is closed. Click anything to close program.")
                sys.exit()

            for player_number, position in enumerate(positions):
                self.map.actual_position(player_number, position)

            os.system("cls")
            print(self.map)
            print("Move: ")

    def get_move(self):
        while True:
            move = input()

            if self.close:
                sys.exit()

            self.server_socket.sendall(move.encode())

            if move == "q":
                self.close = True
                sys.exit()


client = Client(HOST_IP, HOST_PORT)
client.start_connection()
client.start_game()
