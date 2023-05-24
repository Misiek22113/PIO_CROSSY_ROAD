import pickle
import socket
import sys
import time
import threading
import numpy as np

from game_simulation.game import Game

ROUND_TIME = 1

IP = "127.0.0.1"
PORT = 6000

MOVE_SIZE = 34
MAX_PLAYERS = 3
NUMBER_OF_THREADS_TO_CANCEL_CONNECTION = 1
INIT_VALUE_NUMBER_OF_CONNECTIONS = 0
INIT_VALUE_SEMAPHORE = 0


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(MAX_PLAYERS)
        self.client_sockets = [None for _ in range(MAX_PLAYERS)]
        self.game = Game()
        self.number_of_connections = INIT_VALUE_NUMBER_OF_CONNECTIONS
        self.lock = threading.Lock()
        self.round_lock = [threading.Semaphore(INIT_VALUE_SEMAPHORE) for _ in range(MAX_PLAYERS)]
        self.close_connection = np.array([False for _ in range(MAX_PLAYERS)])
        self.close = False
        self.client_threads = [None for _ in range(MAX_PLAYERS)]
        self.active_connections = MAX_PLAYERS
        self.place = [0, 0, 0]
        self.new = [0, 0, 0]
        self.already_connected = 0

    def start_connection(self):
        threading.Thread(target=self.server_command).start()

        for x in range(MAX_PLAYERS + NUMBER_OF_THREADS_TO_CANCEL_CONNECTION):
            threading.Thread(target=self.connect_client).start()

        threading.Thread(target=self.round_timer).start()

        while True:
            if self.number_of_connections > self.already_connected:
                for x, value in enumerate(self.new):
                    if value == 1:
                        self.client_threads[x] = [threading.Thread(target=self.handle_move, args=[x]),
                                            threading.Thread(target=self.send_position, args=[x])]

                        for thread in self.client_threads[x]:
                            thread.start()

                        self.already_connected += 1
                        self.new[x] = 0
                        break

            if self.active_connections != MAX_PLAYERS:
                for x in range(MAX_PLAYERS - self.active_connections):
                    threading.Thread(target=self.connect_client).start()
                self.active_connections = MAX_PLAYERS

            if self.close:
                break

        for group_of_threads in self.client_threads:
            for thread in group_of_threads:
                while thread.is_alive():
                    continue

        self.server_socket.close()

    def connect_client(self):
        while True:
            try:
                client_socket_to_check, _ = self.server_socket.accept()
            except OSError:
                sys.exit()

            self.lock.acquire()
            if self.number_of_connections == MAX_PLAYERS:
                client_socket_to_check.send(b"NO")
                client_socket_to_check.close()
                self.lock.release()
                continue
            else:
                for number, value in enumerate(self.place):
                    if value == 0:
                        client_number = number
                        print(number)
                        break

                self.client_sockets[client_number] = client_socket_to_check
                self.place[client_number] = 1
                self.new[client_number] = 1
                self.game.add_player(client_number)
                self.number_of_connections += 1
                self.lock.release()
                self.client_sockets[client_number].sendall(b"OK")

    def handle_move(self, client_number: int):
        while True:
            print("wait for move")
            move = self.client_sockets[client_number].recv(MOVE_SIZE).decode()
            print("move: " + move)
            self.lock.acquire()
            if move == 'q':
                self.close_connection[client_number] = True
                self.place[client_number] = 0
                print("BYEEEEEE  " + str(client_number + 1))
                self.game.delete_player(client_number)
                self.active_connections -= 1
                self.number_of_connections -= 1
                self.already_connected -= 1
                self.lock.release()
                sys.exit()

            if self.close:
                self.client_sockets[client_number].close()
                self.lock.release()
                sys.exit()

            self.game.make_move(client_number, move)
            self.lock.release()

            self.round_lock[client_number].acquire()

    def send_position(self, client_number):
        while True:
            self.lock.acquire()
            print(sys.getsizeof(self.game.get_positions()))

            if self.close:
                self.client_sockets[client_number].send(pickle.dumps(None))
                self.lock.release()
                sys.exit()

            self.client_sockets[client_number].send(pickle.dumps(self.game.get_positions()))

            if self.close_connection[client_number]:
                self.client_sockets[client_number].close()
                self.close_connection[client_number] = False
                self.lock.release()
                sys.exit()

            self.lock.release()
            self.round_lock[client_number].acquire()

    def round_timer(self):
        while True:
            time.sleep(ROUND_TIME)
            for locking in self.round_lock:
                locking.release()

            if self.close:
                sys.exit()

    def server_command(self):
        while True:
            command = input()
            if command == "q":
                self.close = True
                sys.exit()


server = Server(IP, PORT)
server.start_connection()
