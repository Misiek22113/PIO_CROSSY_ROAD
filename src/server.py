import pickle
import socket
import sys
import threading

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
        self.server_status = False

    def start_connection(self):
        threading.Thread(target=self.get_quit).start()

        try:
            self.client_socket, _ = self.server_socket.accept()
        except OSError:
            sys.exit()

        while True:
            move = pickle.loads(self.client_socket.recv(SIZE_OF_CLIENT_MESSAGE))
            if not move['quit']:
                self.player.move(move)
            else:
                self.client_socket.send(pickle.dumps(1))
                break

            if self.server_status:
                self.client_socket.send(pickle.dumps(2))
                break

            self.client_socket.send(pickle.dumps([self.player.rect.x, self.player.rect.y]))

        if self.server_status:
            print("Click something to close server.")
        self.client_socket.close()

    def get_quit(self):
        while True:
            q = input()
            if q == "q":
                self.server_status = True
                self.server_socket.close()
                break


# TODO delete later
server = Server()
server.start_connection()
