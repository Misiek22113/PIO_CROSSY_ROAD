import pickle
import socket

from player.player import create_player

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6000
SIZE_OF_CLIENT_MESSAGE = 200


class Server:

    def __init__(self):
        self.ip = SERVER_IP
        self.port = SERVER_PORT
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(1)
        self.client_socket = None
        self.player = create_player(100, 100, "spiderman")

    def start_connection(self):
        self.client_socket, _ = self.server_socket.accept()
        while True:
            self.client_socket.send(pickle.dumps([self.player.rect.x, self.player.rect.y]))
            move = pickle.loads(self.client_socket.recv(SIZE_OF_CLIENT_MESSAGE))

            self.player.move(move)


# TODO delete later
server = Server()
server.start_connection()
