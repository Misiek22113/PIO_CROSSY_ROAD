import pickle
import socket
import sys
import threading

import numpy as np

# server consts
QUIT = "q"

SERVER_IS_CLOSING = True
SERVER_IS_RUNNING = False

MAX_PLAYERS = 3

GAME_IS_ENDED = 1
NEW_GAME = 1

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6001
BUFFER_SIZE = 4096

# connection consts
CONNECTION_IS_DEACTIVATED = False
CONNECTION_IS_ACTIVE = True

NEW_CONNECTION = 1
NO_CONNECTIONS = 0

CLOSED_CONNECTION = 1

CONNECTION_IS_SUCCESSFUL = b"OK"
SERVER_IS_FULL = b"NO"

GAME_NOT_TO_START = False
GAME_TO_START = True

NUMBER_OF_THREADS_TO_CANCEL_CONNECTION = 1
NUMBER_OF_STARTED_CONNECTIONS_INIT_VALUE = 0
NUMBER_OF_STARTED_GAMES_INIT_VALUE = 0

FREE = True
BUSY = False

PLACE_FOR_SOCKET = None

# client consts
BACK_TO_CHAMPION_SELECT = "B"
CHOSEN_CHAMPIONS_INFORMATION_REQUEST = "P"

CHAMPION_IS_AVAILABLE = b"YES"
CHAMPION_IS_NOT_AVAILABLE = b"NO"
CHAMPION_IS_NOT_CHOSEN = -1

CLIENT_QUIT = -1
SERVER_QUIT_SIGNAL_IN_CHAMPION_SELECT = b"Q"
SERVER_QUIT_SIGNAL_IN_LOBBY = [None, None, None]

LOBBY = 0
CONTINUE = 1
BREAK = -1


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
        self.client_sockets = np.array([PLACE_FOR_SOCKET for _ in range(MAX_PLAYERS)])

        # variables for connections management
        self.number_of_started_connections = NUMBER_OF_STARTED_CONNECTIONS_INIT_VALUE
        self.connections_needed_to_start = NO_CONNECTIONS
        self.number_of_started_games = NUMBER_OF_STARTED_GAMES_INIT_VALUE
        self.client_number = np.array([FREE for _ in range(MAX_PLAYERS)])
        self.game_to_start = np.array([GAME_NOT_TO_START for _ in range(MAX_PLAYERS)])

        # variables for game
        self.chosen_champions = [CHAMPION_IS_NOT_CHOSEN for _ in range(MAX_PLAYERS)]

    def start_server(self):
        threading.Thread(target=self.open_server_commands).start()

        for x in range(MAX_PLAYERS + NUMBER_OF_THREADS_TO_CANCEL_CONNECTION):
            threading.Thread(target=self.connect_client).start()

        while True:
            self.start_games()
            self.open_new_connections()

            if self.server_status == SERVER_IS_CLOSING:
                break

        self.server_socket.close()

    def open_new_connections(self):
        if self.connections_needed_to_start != NO_CONNECTIONS:
            for x in range(self.connections_needed_to_start):
                threading.Thread(target=self.connect_client).start()

            self.connections_needed_to_start = NO_CONNECTIONS

    def start_games(self):
        if self.number_of_started_connections > self.number_of_started_games:
            for player_number, status_of_game in enumerate(self.game_to_start):
                if status_of_game == GAME_TO_START:
                    threading.Thread(target=self.handle_client, args=[player_number]).start()
                    self.number_of_started_games += NEW_GAME
                    self.game_to_start[player_number] = GAME_NOT_TO_START
                    break

    def connect_client(self):
        while True:
            try:
                client_new_connection, _ = self.server_socket.accept()
            except OSError:
                self.connections_needed_to_start += CLOSED_CONNECTION
                sys.exit()

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
                self.number_of_started_connections += NEW_CONNECTION
                self.client_sockets[client_number].sendall(CONNECTION_IS_SUCCESSFUL)

    def handle_client(self, client_number):
        connection = CONNECTION_IS_ACTIVE
        while connection:
            try:
                champion_select_result = self.champion_select(client_number)

                if champion_select_result == CONTINUE:
                    continue
                elif champion_select_result == BREAK:
                    break

                while True:
                    lobby_result = self.lobby(client_number)
                    if lobby_result == CONNECTION_IS_DEACTIVATED:
                        connection = CONNECTION_IS_DEACTIVATED
                        break
                    elif lobby_result == BACK_TO_CHAMPION_SELECT:
                        break

            except ConnectionResetError:
                break

        self.client_number[client_number] = FREE
        self.connections_needed_to_start += CLOSED_CONNECTION
        self.number_of_started_connections -= CLOSED_CONNECTION
        self.number_of_started_games -= GAME_IS_ENDED
        self.client_sockets[client_number].close()
        sys.exit()

    def champion_select(self, client_number):
        chosen_champion = pickle.loads(self.client_sockets[client_number].recv(BUFFER_SIZE))

        if chosen_champion == CLIENT_QUIT:
            return BREAK

        if self.server_status == SERVER_IS_CLOSING:
            self.client_sockets[client_number].sendall(SERVER_QUIT_SIGNAL_IN_CHAMPION_SELECT)
            return BREAK

        if chosen_champion in self.chosen_champions:
            self.client_sockets[client_number].sendall(CHAMPION_IS_NOT_AVAILABLE)
            return CONTINUE

        else:
            self.client_sockets[client_number].sendall(CHAMPION_IS_AVAILABLE)
            self.chosen_champions[client_number] = chosen_champion
            return LOBBY

    def lobby(self, client_number):
        client_signal = self.client_sockets[client_number].recv(BUFFER_SIZE).decode()

        if self.server_status == SERVER_IS_CLOSING:
            self.client_sockets[client_number].send(pickle.dumps(SERVER_QUIT_SIGNAL_IN_LOBBY))
            return CONNECTION_IS_DEACTIVATED

        if client_signal == CHOSEN_CHAMPIONS_INFORMATION_REQUEST:
            self.client_sockets[client_number].send(pickle.dumps(self.chosen_champions))
            return LOBBY
        elif client_signal == BACK_TO_CHAMPION_SELECT:
            self.chosen_champions[client_number] = CHAMPION_IS_NOT_CHOSEN
            return BACK_TO_CHAMPION_SELECT
        else:
            self.chosen_champions[client_number] = CHAMPION_IS_NOT_CHOSEN
            return CONNECTION_IS_DEACTIVATED

    def open_server_commands(self):
        while True:
            command = input()
            if command == QUIT:
                self.server_status = SERVER_IS_CLOSING
                sys.exit()


# TODO delete later
server = Server()
server.start_server()
