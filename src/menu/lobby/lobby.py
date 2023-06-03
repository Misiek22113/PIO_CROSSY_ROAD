import pickle
import sys

import pygame

from src.menu.window.window import Window
from src.menu.button.button import Button

CHOSEN_CHAMPIONS_INFORMATION_REQUEST = b"P"
CHECK_CONNECTION = 0
QUIT = b"Q"
BACK = b"B"
PLAYER_IS_NOT_CONNECTED = -1
PLAYER_POSITION_IN_LOBBY = 400
EMPTY_BUTTON = None


class Lobby(Window):

    def __init__(self, width, height):
        super().__init__("lobby", width, height)
        self.width = width
        self.height = height
        self.LEAVE_BUTTON = EMPTY_BUTTON
        self.LOBBY_MOUSE_POS = EMPTY_BUTTON

    def print_lobby_menu(self):
        self.screen.blit(self.BACKGROUND_IMAGE, self.BACKGROUND_IMAGE_POS)
        self.draw_text("Waiting for other players...", 640, 100, self.FONT_OPTION, self.TEXT_COLOR)
        self.draw_text("Player 1", 240, 200, self.FONT_OPTION, self.TEXT_COLOR)
        self.draw_text("Player 2", 640, 200, self.FONT_OPTION, self.TEXT_COLOR)
        self.draw_text("Player 3", 1040, 200, self.FONT_OPTION, self.TEXT_COLOR)
        self.LEAVE_BUTTON = Button(image=self.MENU_BUTTON, pos=(640, 650), text_input="LEAVE", font=self.FONT_OPTION,
                                   base_color=self.BASE_COLOR, hovering_color=self.HOVERING_COLOR)

    def draw_player(self, x, y, champion_index):
        scale = 10
        img = self.CHAMPIONS[champion_index][0]
        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        img_rect = img.get_rect(center=(x, y))
        self.screen.blit(img, img_rect)
        self.draw_text(self.CHAMPIONS[champion_index][1], x, 500, self.FONT_OPTION, self.TEXT_COLOR)

    def handle_lobby_loop(self, socket):
        while True:
            self.print_lobby_menu()

            self.LOBBY_MOUSE_POS = pygame.mouse.get_pos()

            self.LEAVE_BUTTON.change_color(self.LOBBY_MOUSE_POS)
            self.LEAVE_BUTTON.update(self.screen)

            try:
                socket.sendall(CHOSEN_CHAMPIONS_INFORMATION_REQUEST)
                chosen_champions = pickle.loads(socket.recv(4096))
                start_game = pickle.loads(socket.recv(4096))
            except (ConnectionResetError, ConnectionAbortedError):
                socket.close()
                return "lost_connection_with_server", None

            if chosen_champions[CHECK_CONNECTION] is None:
                socket.close()
                return "server_is_closed", None

            for player_number, chosen_champion in enumerate(chosen_champions):
                if chosen_champion != PLAYER_IS_NOT_CONNECTED:
                    self.draw_player(240 + (PLAYER_POSITION_IN_LOBBY * player_number), 350, chosen_champion)

            if start_game == 1:
                champions_names = []
                for chosen_champion in chosen_champions:
                    champions_names.append(self.CHAMPIONS[chosen_champion][1])

                return "game", champions_names

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.LEAVE_BUTTON.check_for_input(self.LOBBY_MOUSE_POS):
                        try:
                            socket.sendall(BACK)
                        except (ConnectionResetError, ConnectionAbortedError):
                            socket.close()
                            return "lost_connection_with_server", None

                        return "champion_select", None

                if event.type == pygame.QUIT:
                    try:
                        socket.sendall(QUIT)
                    except (ConnectionResetError, ConnectionAbortedError):
                        pass

                    socket.close()
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
