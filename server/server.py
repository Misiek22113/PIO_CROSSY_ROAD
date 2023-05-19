import os
import pickle
import socket
import sys
import time
from typing import NoReturn
import threading
from game import Game

ROUND_TIME = 1

IP = '127.0.0.1'
PORT = 6000

MOVE_SIZE = 34
MAX_PLAYERS = 3
INIT_VALUE__NUMBER_OF_CONNECTIONS = 0
INIT_VALUE_SEMAPHORE = 0

class Server:
    def __init__(self, ip: str, port: int) -> NoReturn:
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(MAX_PLAYERS)
        self.client_sockets = [None for _ in range(MAX_PLAYERS)]
        self.game = Game()
        self.number_of_connections = INIT_VALUE__NUMBER_OF_CONNECTIONS
        self.lock = threading.Lock()
        self.round_lock = [threading.Semaphore(INIT_VALUE_SEMAPHORE) for _ in range(MAX_PLAYERS)]

    def start_connection(self) -> NoReturn:
        for x in range(MAX_PLAYERS+1):
            threading.Thread(target=self.connect_client).start()

        already_connected = 0
        threading.Thread(target=self.round_timer).start()

        while True:
            if self.number_of_connections > already_connected:
                threading.Thread(target=self.handle_move, args=[already_connected]).start()
                threading.Thread(target=self.send_position, args=[already_connected]).start()
                already_connected += 1
            elif self.number_of_connections == MAX_PLAYERS:
                break

    def connect_client(self) -> NoReturn:
        while True:
            client_socket_to_check, _ = self.server_socket.accept()
            self.lock.acquire()
            if self.number_of_connections == 3:
                client_socket_to_check.send(b'NO')
                client_socket_to_check.close()
                self.lock.release()
                continue
            else:
                client_number = self.number_of_connections
                self.client_sockets[client_number] = client_socket_to_check
                self.number_of_connections += 1
                self.game.add_player(self.number_of_connections)
                self.lock.release()
                self.client_sockets[client_number].sendall(b'OK')

    def handle_move(self, client_number: int):
        while True:
            print('wait for move')
            move = self.client_sockets[client_number].recv(MOVE_SIZE).decode()
            print('move: ' + move)
            self.lock.acquire()
            self.game.make_move(client_number, move)
            self.lock.release()

            self.round_lock[client_number].acquire()

    def send_position(self, client_number):
        while True:
            self.lock.acquire()
            print(sys.getsizeof(self.game.get_positions()))
            self.client_sockets[client_number].send(pickle.dumps(self.game.get_positions()))
            self.lock.release()
            self.round_lock[client_number].acquire()

    def round_timer(self):
        while True:
            time.sleep(ROUND_TIME)
            for locking in self.round_lock:
                locking.release()


server = Server(IP, PORT)
server.start_connection()
