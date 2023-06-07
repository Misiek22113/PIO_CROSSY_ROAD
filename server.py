import pickle
import socket
import sys
import threading
import time

import numpy as np

from src.game_simulation.test_obstacles import TestObstacles
from src.player.player import create_player

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

LOBBY = 1
CHAMPION_SELECT = 2
LEFT_CHAMPION_SELECT = -1
CLIENT_DISCONNECT_IN_CHAMPION_SELECT = 15
START_GAME = 5

OBSTACLE_GENERATE_DELAY = 1
FINISH_LINE_GENERATE_DELAY = 5
SECOND = 1
COUNTING_START = 0
WAIT_FOR_ANOTHER_CHECK = 1
FRAME_TIME = 1 / 60

GAME_IS_GOING = 0
GAME_IS_NOT_STARTED = False
GAME_IS_STARTED = True

START_GAME_SIGNAL = 1
WAIT_SIGNAL = 0

EVERY_PLAYER_CONNECTED = MAX_PLAYERS
PLAYER_IS_NOT_IN_LOBBY = 1

PLAYER_WIN_SIGNAL = [10, 10]
PLAYER_LOSE_SIGNAL = [9, 9]
QUIT_SIGNAL_IN_GAME = (8, 8, 8)

PLAYER_POSITION_Y = 200
STARTING_Y = 200
STARTING_X = 100
NO_PLAYER_CREATE = [None, None, None]

CHAMPIONS = ["cute_boy", "engineer", "frog", "girl", "spiderman", "student"]


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
        self.players = NO_PLAYER_CREATE
        self.elapsed_time_from_last_obstacle_generation = COUNTING_START
        self.elapsed_total_time = COUNTING_START
        self.test_obstacles = TestObstacles()

        self.game_is_started = GAME_IS_NOT_STARTED
        self.game_is_ended = GAME_IS_ENDED

    def start_server(self):
        threading.Thread(target=self.open_server_commands).start()
        threading.Thread(target=self.timed_generate_obstacles).start()

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
                try:
                    client_new_connection.send(SERVER_IS_FULL)
                except (ConnectionResetError, ConnectionAbortedError):
                    pass
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
        game_start = GAME_IS_NOT_STARTED

        while connection:
            champion_select_result = self.champion_select(client_number)

            if champion_select_result == CHAMPION_SELECT:
                continue
            elif champion_select_result == LEFT_CHAMPION_SELECT:
                break

            while True:
                lobby_result = self.lobby(client_number)
                if lobby_result == CONNECTION_IS_DEACTIVATED:
                    connection = CONNECTION_IS_DEACTIVATED
                    break
                elif lobby_result == BACK_TO_CHAMPION_SELECT:
                    break
                elif lobby_result == START_GAME:
                    game_start = GAME_IS_STARTED
                    break

            if game_start:
                self.game_is_ended = GAME_IS_GOING
                self.game(client_number)
                connection = CONNECTION_IS_DEACTIVATED

        self.client_number[client_number] = FREE
        self.connections_needed_to_start += CLOSED_CONNECTION
        self.number_of_started_connections -= CLOSED_CONNECTION
        self.number_of_started_games -= GAME_IS_ENDED
        self.client_sockets[client_number].close()
        self.chosen_champions[client_number] = CHAMPION_IS_NOT_CHOSEN
        self.game_is_ended = GAME_IS_ENDED
        sys.exit()

    def champion_select(self, client_number):
        try:
            chosen_champion = pickle.loads(self.client_sockets[client_number].recv(BUFFER_SIZE))

            if chosen_champion == CLIENT_QUIT:
                return LEFT_CHAMPION_SELECT

            if self.server_status == SERVER_IS_CLOSING:
                self.client_sockets[client_number].sendall(SERVER_QUIT_SIGNAL_IN_CHAMPION_SELECT)
                return LEFT_CHAMPION_SELECT

            if chosen_champion in self.chosen_champions:
                self.client_sockets[client_number].sendall(CHAMPION_IS_NOT_AVAILABLE)
                return CHAMPION_SELECT
            else:
                self.client_sockets[client_number].sendall(CHAMPION_IS_AVAILABLE)
                self.chosen_champions[client_number] = chosen_champion
                return LOBBY
        except (ConnectionResetError, ConnectionAbortedError):
            return LEFT_CHAMPION_SELECT

    def lobby(self, client_number):
        try:
            client_signal = self.client_sockets[client_number].recv(BUFFER_SIZE).decode()

            if self.server_status == SERVER_IS_CLOSING:
                self.client_sockets[client_number].send(pickle.dumps(SERVER_QUIT_SIGNAL_IN_LOBBY))
                self.client_sockets[client_number].recv(BUFFER_SIZE)
                self.client_sockets[client_number].send(pickle.dumps(SERVER_QUIT_SIGNAL_IN_LOBBY))
                return CONNECTION_IS_DEACTIVATED

            if client_signal == CHOSEN_CHAMPIONS_INFORMATION_REQUEST:
                players_in_lobby = EVERY_PLAYER_CONNECTED
                for champion in self.chosen_champions:
                    if champion == CHAMPION_IS_NOT_CHOSEN:
                        players_in_lobby -= PLAYER_IS_NOT_IN_LOBBY

                if players_in_lobby == EVERY_PLAYER_CONNECTED:
                    self.client_sockets[client_number].send(pickle.dumps([self.chosen_champions, START_GAME_SIGNAL]))
                    return START_GAME
                else:
                    self.client_sockets[client_number].send(pickle.dumps([self.chosen_champions, WAIT_SIGNAL]))
                    return LOBBY
            elif client_signal == BACK_TO_CHAMPION_SELECT:
                self.chosen_champions[client_number] = CHAMPION_IS_NOT_CHOSEN
                return BACK_TO_CHAMPION_SELECT
            else:
                self.chosen_champions[client_number] = CHAMPION_IS_NOT_CHOSEN
                return CONNECTION_IS_DEACTIVATED
        except (ConnectionResetError, ConnectionAbortedError):
            return CONNECTION_IS_DEACTIVATED

    def game(self, client_number):
        for number in range(MAX_PLAYERS):
            self.players[number] = create_player(STARTING_X, STARTING_Y + (PLAYER_POSITION_Y * number),
                                                 CHAMPIONS[self.chosen_champions[number]])

        self.game_is_started = GAME_IS_STARTED

        while self.game_is_started:
            try:
                move = pickle.loads(self.client_sockets[client_number].recv(BUFFER_SIZE))
            except (ConnectionResetError, ConnectionAbortedError, EOFError):
                move = {"quit": True}

            if move["quit"]:
                move["has_won"] = False
                move["moving_right"] = False
                move["moving_left"] = True
                move["moving_up"] = False
                move["moving_down"] = False
                move["is_colliding_with_pushing"] = False
                move["is_colliding"] = False
                while self.game_is_ended:
                    self.players[client_number].move(move)
                    self.test_obstacles.handle_obstacles()
                    time.sleep(0.01)
                break

            obstacles_names, obstacles_positions = self.handle_move(move, client_number)
            end_game_result = self.handle_end_game(move, client_number)
            if end_game_result == GAME_IS_ENDED:
                break

            result_send_info_to_player = self.send_info_to_player(client_number, obstacles_names, obstacles_positions)

            if result_send_info_to_player == QUIT:
                return

            self.test_obstacles.handle_obstacles()

    def handle_move(self, move, client_number):
        obstacles_names = self.test_obstacles.names
        obstacles_positions = []

        for obstacle in self.test_obstacles.obstacles:
            obstacles_positions.append([obstacle.x, obstacle.y])

        for obstacle in self.test_obstacles.obstacles:
            if self.players[client_number].rect.colliderect(obstacle.rect):
                move["is_colliding"] = True

                if obstacle.rect.x > self.players[client_number].rect.x:
                    move["moving_right"] = False
                    move["is_colliding_with_pushing"] = True
                elif obstacle.rect.x < self.players[client_number].rect.x:
                    move["moving_left"] = False

                if obstacle.rect.y < self.players[client_number].rect.y:
                    move["moving_up"] = False
                elif obstacle.rect.y > self.players[client_number].rect.y:
                    move["moving_down"] = False

                if obstacle.is_finish_line:
                    move["has_won"] = True
                break
            else:
                move["is_colliding"] = False
                move["is_colliding_with_pushing"] = False

        self.players[client_number].move(move)
        return obstacles_names, obstacles_positions

    def handle_end_game(self, move, client_number):
        if self.game_is_ended == GAME_IS_ENDED:
            try:
                self.client_sockets[client_number].send(
                    pickle.dumps((*PLAYER_LOSE_SIGNAL, self.chosen_champions[client_number])))
            except (ConnectionResetError, ConnectionAbortedError):
                pass
            return GAME_IS_ENDED

        if move["has_won"]:
            self.game_is_ended = GAME_IS_ENDED
            try:
                self.client_sockets[client_number].send(
                    pickle.dumps((*PLAYER_WIN_SIGNAL, self.chosen_champions[client_number])))
            except (ConnectionResetError, ConnectionAbortedError):
                pass
            return GAME_IS_ENDED

        return GAME_IS_GOING

    def send_info_to_player(self, client_number, obstacles_names, obstacles_positions):
        if self.server_status == SERVER_IS_CLOSING:
            try:
                self.client_sockets[client_number].send(pickle.dumps(QUIT_SIGNAL_IN_GAME))
            except (ConnectionResetError, ConnectionAbortedError):
                pass

            self.game_is_started = GAME_IS_NOT_STARTED
            return QUIT

        player_positions = []
        for player in self.players:
            player_positions.append([player.x, player.y])

        try:
            self.client_sockets[client_number].send(
                pickle.dumps((player_positions, obstacles_names, obstacles_positions)))
        except (ConnectionResetError, ConnectionAbortedError):
            pass

        return None

    def timed_generate_obstacles(self):
        while self.server_status == SERVER_IS_RUNNING:
            self.test_obstacles.obstacles = []
            self.test_obstacles.names = []
            self.elapsed_total_time = COUNTING_START
            self.elapsed_time_from_last_obstacle_generation = COUNTING_START
            time.sleep(WAIT_FOR_ANOTHER_CHECK)
            while self.game_is_ended == GAME_IS_GOING:
                if self.elapsed_total_time >= FINISH_LINE_GENERATE_DELAY:
                    self.test_obstacles.add_obstacle(generate_finish_line=True)
                    self.elapsed_total_time = COUNTING_START
                    self.elapsed_time_from_last_obstacle_generation = COUNTING_START

                if self.elapsed_time_from_last_obstacle_generation >= OBSTACLE_GENERATE_DELAY:
                    self.test_obstacles.add_obstacle()
                    self.elapsed_time_from_last_obstacle_generation = COUNTING_START

                self.test_obstacles.handle_obstacles()
                self.elapsed_total_time += SECOND
                self.elapsed_time_from_last_obstacle_generation += SECOND
                time.sleep(SECOND)

    def open_server_commands(self):
        while True:
            command = input()
            if command == QUIT:
                self.server_status = SERVER_IS_CLOSING
                sys.exit()


# TODO delete later
server = Server()
server.start_server()
