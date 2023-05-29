import pickle
import socket
import sys
import threading

from player.player import create_player

PLAYER_IS_CLOSING = True

PLAYER_IS_RUNNING = False

SERVER_IS_RUNNING = False

PLACE_FOR_SOCKET = None

SERVER_IS_CLOSING = True

QUIT_COMMAND = "q"

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6000
SIZE_OF_CLIENT_MESSAGE = 200

CLIENT_QUIT = 1
SERVER_QUIT = 2
PLAYER_POSITION_X = 100
PLAYER_POSITION_Y = 100
NUMBER_OF_PLAYERS = 1


class Server:

    def __init__(self):
        self.ip = SERVER_IP
        self.port = SERVER_PORT
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(NUMBER_OF_PLAYERS)
        self.client_socket = PLACE_FOR_SOCKET
        self.player = create_player(PLAYER_POSITION_X, PLAYER_POSITION_Y, "spiderman")
        self.server_closing = SERVER_IS_RUNNING
        self.player_closing = PLAYER_IS_RUNNING

    def start_connection(self):
        threading.Thread(target=self.get_quit).start()

        try:
            self.client_socket, _ = self.server_socket.accept()
        except OSError:
            sys.exit()

        while True:
            try:
                move = pickle.loads(self.client_socket.recv(SIZE_OF_CLIENT_MESSAGE))
            except ConnectionResetError:
               self.player_closing = PLAYER_IS_CLOSING
               break

            if not move["quit"]:
                self.player.move(move)
            else:
                self.client_socket.send(pickle.dumps(CLIENT_QUIT))
                self.player_closing = PLAYER_IS_CLOSING
                break

            if self.server_closing:
                self.client_socket.send(pickle.dumps(SERVER_QUIT))
                break

            try:
                self.client_socket.send(pickle.dumps([self.player.rect.x, self.player.rect.y]))
            except ConnectionResetError:
                self.player_closing = PLAYER_IS_CLOSING
                break

        if self.player_closing:
            print("Click something to close server.")

        self.client_socket.close()

    def get_quit(self):
        while True:
            q = input()
            if q == QUIT_COMMAND or self.player_closing:
                self.server_closing = SERVER_IS_CLOSING
                self.server_socket.close()
                break


# TODO delete later
server = Server()
server.start_connection()
