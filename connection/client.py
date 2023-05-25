import os
import socket
import sys
import threading
import pickle

from game_simulation.game import Game

QUIT = "q"
CLOSE_SIGNAL = None

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
        self.map = Game()
        self.server_socket = SERVER_IS_NOT_CONNECT
        self.client_status = CLIENT_IS_RUNNING

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

    def start_game(self):
        threading.Thread(target=self.receive_move).start()
        threading.Thread(target=self.receive_players_positions).start()

    def receive_players_positions(self):
        while True:
            if self.client_status == CLIENT_IS_CLOSING:
                self.server_socket.close()
                sys.exit()

            positions = pickle.loads(self.server_socket.recv(SIZE_OF_RECV_WITH_POSITIONS))

            if positions == CLOSE_SIGNAL:
                self.server_socket.sendall(CLOSING_MESSAGE)
                self.client_status = CLIENT_IS_CLOSING
                print("Server is closed. Click anything to close program.")
                sys.exit()

            for player_number, position in enumerate(positions):
                self.map.actual_position(player_number, position)

            os.system("cls")
            print(self.map)
            print("Move: ")

    def receive_move(self):
        while True:
            move = input()

            if self.client_status == CLIENT_IS_CLOSING:
                self.server_socket.close()
                sys.exit()

            self.server_socket.sendall(move.encode())

            if move == QUIT:
                self.client_status = CLIENT_IS_CLOSING
                sys.exit()


# TODO delete later
client = Client()
client.start_connection()
client.start_game()
