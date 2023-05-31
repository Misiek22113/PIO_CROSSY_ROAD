import pickle
import socket
import sys
import time
import threading
import numpy as np

NEW_CONNECTION = 1

CONNECTION_IS_SUCCESSFUL = b"OK"
SERVER_IS_FULL = b"NO"

SERVER_IS_CLOSING = True
SERVER_IS_RUNNING = False

CLOSED_CONNECTION = 1
QUIT = "q"
CLOSE_SIGNAL = None

GAME_IS_ENDED = 1
ROUND_TIME = 1
MAX_PLAYERS = 3
SEMAPHORE_INIT_VALUE = 0
NEW_GAME = 1

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6001
SIZE_OF_CLIENT_MESSAGE = 34

NUMBER_OF_THREADS_TO_CANCEL_CONNECTION = 1
NUMBER_OF_STARTED_CONNECTIONS_INIT_VALUE = 0
NUMBER_OF_STARTED_GAMES_INIT_VALUE = 0
NOT_NEED_OF_NEW_CONNECTIONS = 0

CLIENT_IS_CONNECT = False
CLIENT_IS_CLOSING = True

FREE = True
BUSY = False

GAME_NOT_TO_START = False
GAME_TO_START = True

EMPTY_PLACE_FOR_THREADS = np.array([None])
EMPTY_PLACE_FOR_SOCKET = None


class Server:

    def __init__(self):
        # server's variables
        self.ip = SERVER_IP
        self.port = SERVER_PORT
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(MAX_PLAYERS)
        self.server_status = SERVER_IS_RUNNING

        # clients' variables
        self.client_sockets = np.array([EMPTY_PLACE_FOR_SOCKET for _ in range(MAX_PLAYERS)])
        self.client_status = np.array([CLIENT_IS_CONNECT for _ in range(MAX_PLAYERS)])
        self.client_threads = np.array([EMPTY_PLACE_FOR_THREADS for _ in range(MAX_PLAYERS)])

        # variables for connections management
        self.number_of_started_connections = NUMBER_OF_STARTED_CONNECTIONS_INIT_VALUE
        self.connections_needed_to_start = NOT_NEED_OF_NEW_CONNECTIONS
        self.number_of_started_games = NUMBER_OF_STARTED_GAMES_INIT_VALUE
        self.client_number = np.array([FREE for _ in range(MAX_PLAYERS)])
        self.game_to_start = np.array([GAME_NOT_TO_START for _ in range(MAX_PLAYERS)])

        # variables for game
        self.game_lock = threading.Lock()
        self.chosen_champs = [-1, -1, -1]

    def start_server(self):
        threading.Thread(target=self.open_server_commands).start()

        for x in range(MAX_PLAYERS + NUMBER_OF_THREADS_TO_CANCEL_CONNECTION):
            threading.Thread(target=self.connect_client).start()

        while True:
            self.start_games()
            self.open_new_connections()

            if self.server_status == SERVER_IS_CLOSING:
                break

        # wait for clients disconnection for closing server
        for client_threads in self.client_threads:
            for thread in client_threads:
                if thread:
                    while thread.is_alive():
                        continue

        self.server_socket.close()

    def open_new_connections(self):
        if self.connections_needed_to_start != NOT_NEED_OF_NEW_CONNECTIONS:
            for x in range(self.connections_needed_to_start):
                threading.Thread(target=self.connect_client).start()

            self.game_lock.acquire()
            self.connections_needed_to_start = NOT_NEED_OF_NEW_CONNECTIONS
            self.game_lock.release()

    def start_games(self):
        if self.number_of_started_connections > self.number_of_started_games:
            for player_number, status_of_game in enumerate(self.game_to_start):
                if status_of_game == GAME_TO_START:
                    self.client_threads[player_number] = np.array(
                        [threading.Thread(target=self.handle_client, args=[player_number])])

                    for thread in self.client_threads[player_number]:
                        thread.start()

                    self.number_of_started_games += NEW_GAME
                    self.game_to_start[player_number] = GAME_NOT_TO_START
                    break

    def connect_client(self):
        while True:
            try:
                client_new_connection, _ = self.server_socket.accept()
            except OSError:
                self.game_lock.acquire()
                self.connections_needed_to_start += CLOSED_CONNECTION
                self.game_lock.release()
                sys.exit()

            self.game_lock.acquire()
            if self.number_of_started_connections == MAX_PLAYERS:
                client_new_connection.send(SERVER_IS_FULL)
                client_new_connection.close()
            else:
                for number, status in enumerate(self.client_number):
                    if status == FREE:
                        client_number = number
                        break

                self.client_sockets[client_number] = client_new_connection
                self.client_number[client_number] = BUSY
                self.game_to_start[client_number] = GAME_TO_START
                self.client_status[client_number] = CLIENT_IS_CONNECT
                self.number_of_started_connections += NEW_CONNECTION
                self.client_sockets[client_number].sendall(CONNECTION_IS_SUCCESSFUL)
            self.game_lock.release()

    def handle_client(self, client_number):
        game = True
        while game:
            chosen_champ = pickle.loads(self.client_sockets[client_number].recv(124))
            if chosen_champ == -1:
                break

            if self.server_status == SERVER_IS_CLOSING:
                try:
                    self.client_sockets[client_number].sendall(b"Q")
                except ConnectionResetError:
                    pass
                return

            if chosen_champ in self.chosen_champs:
                try:
                    self.client_sockets[client_number].sendall(b"NO")
                except ConnectionResetError:
                    break

                continue
            else:
                try:
                    self.client_sockets[client_number].sendall(b"YES")
                except ConnectionResetError:
                    break

                self.chosen_champs[client_number] = chosen_champ

            while True:
                try:
                    sended = self.client_sockets[client_number].recv(40).decode()
                except ConnectionResetError:
                    game = False
                    break

                if self.server_status == SERVER_IS_CLOSING:
                    try:
                        self.client_sockets[client_number].send(pickle.dumps([None, None, None]))
                    except ConnectionResetError:
                        pass
                    return

                if sended == "P":
                    try:
                        self.client_sockets[client_number].send(pickle.dumps(self.chosen_champs))
                    except ConnectionResetError:
                        game = False
                        break
                elif sended == "B":
                    self.chosen_champs[client_number] = -1
                    break
                else:
                    game = False
                    self.chosen_champs[client_number] = -1
                    break

        self.client_status[client_number] = CLIENT_IS_CLOSING
        self.client_number[client_number] = FREE
        self.connections_needed_to_start += CLOSED_CONNECTION
        self.number_of_started_connections -= CLOSED_CONNECTION
        self.number_of_started_games -= GAME_IS_ENDED
        self.client_sockets[client_number].close()
        sys.exit()

    def open_server_commands(self):
        while True:
            command = input()
            if command == QUIT:
                self.server_status = SERVER_IS_CLOSING
                sys.exit()


# TODO delete later
server = Server()
server.start_server()
