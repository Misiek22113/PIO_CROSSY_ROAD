import pickle

import pygame
import sys
from src.menu.button.button import Button
from src.menu.window.window import Window

CHAMPION_IS_AVAILABLE = "YES"
SERVER_IS_CLOSED = "Q"
QUIT = -1
BUFFER_SIZE = 4096
BACK = -1

EMPTY_BUTTON = None
CHARACTER_SCALE = 10
CHAMPION_INDEX_OFFSET = 1


def quit_game(socket):
    try:
        socket.sendall(pickle.dumps(QUIT))
    except ConnectionResetError:
        pass

    socket.close()
    pygame.quit()
    sys.exit()


class ChampionSelect(Window):
    def __init__(self, width, height):
        super().__init__("Champion Select", width, height)
        self.champion_index = 0
        self.BUTTON_ARROW_RIGHT = EMPTY_BUTTON
        self.BUTTON_ARROW_LEFT = EMPTY_BUTTON
        self.BACK_BUTTON = EMPTY_BUTTON
        self.NEXT_BUTTON = EMPTY_BUTTON
        self.CHAMPION_SELECT_MOUSE_POS = None
        self.width = width
        self.height = height

    def print_champion_select_menu(self):
        self.screen.blit(self.BACKGROUND_IMAGE, self.BACKGROUND_IMAGE_POS)
        self.draw_text("Choose your Champion", 640, 100, self.FONT_CHAMPION_SELECT, self.TEXT_COLOR)
        self.draw_text(self.CHAMPIONS[self.champion_index][1].replace("_", " "), 640, 500, self.FONT_CHAMPION_SELECT, self.TEXT_COLOR)
        self.BACK_BUTTON = Button(image=self.MENU_BUTTON, pos=(440, 650), text_input="BACK", font=self.FONT_OPTION,
                                  base_color=self.BASE_COLOR, hovering_color=self.HOVERING_COLOR)
        self.NEXT_BUTTON = Button(image=self.MENU_BUTTON, pos=(840, 650), text_input="NEXT", font=self.FONT_OPTION,
                                  base_color=self.BASE_COLOR, hovering_color=self.HOVERING_COLOR)
        self.BUTTON_ARROW_LEFT = Button(image=None, pos=(400, 350), text_input="<", font=self.FONT_OPTION,
                                        base_color=self.BASE_COLOR, hovering_color=self.HOVERING_COLOR)
        self.BUTTON_ARROW_RIGHT = Button(image=None, pos=(880, 350), text_input=">", font=self.FONT_OPTION,
                                         base_color=self.BASE_COLOR, hovering_color=self.HOVERING_COLOR)
        img = self.CHAMPIONS[self.champion_index][0]
        img = pygame.transform.scale(
            img, (int(img.get_width() * CHARACTER_SCALE), int(img.get_height() * CHARACTER_SCALE))
        )
        img_rect = img.get_rect(center=(640, 350))
        self.screen.blit(img, img_rect)

    def change_champion_index(self, to_change):
        max_index = len(self.CHAMPIONS) - 1
        if max_index >= to_change >= 0:
            self.champion_index = to_change
        elif to_change > max_index:
            self.champion_index = 0
        elif to_change < 0:
            self.champion_index = max_index

    def handle_champion_select_loop(self, socket):
        while True:
            self.print_champion_select_menu()
            self.CHAMPION_SELECT_MOUSE_POS = pygame.mouse.get_pos()
            self.print_buttons()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game(socket)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.BACK_BUTTON.check_for_input(self.CHAMPION_SELECT_MOUSE_POS):
                        try:
                            socket.sendall(pickle.dumps(BACK))
                        except (ConnectionResetError, ConnectionAbortedError):
                            pass

                        socket.close()
                        return "menu"
                    if self.NEXT_BUTTON.check_for_input(self.CHAMPION_SELECT_MOUSE_POS):
                        try:
                            socket.sendall(pickle.dumps(self.champion_index))
                            server_signal = socket.recv(BUFFER_SIZE).decode()
                        except (ConnectionResetError, ConnectionAbortedError):
                            socket.close()
                            return "lost_connection_with_server"

                        if server_signal == SERVER_IS_CLOSED:
                            socket.close()
                            return "server_is_closed"

                        if server_signal == CHAMPION_IS_AVAILABLE:
                            return "lobby"
                        else:
                            return "champion_is_picked"

                    if self.BUTTON_ARROW_RIGHT.check_for_input(self.CHAMPION_SELECT_MOUSE_POS):
                        self.change_champion_index(self.champion_index + CHAMPION_INDEX_OFFSET)
                    if self.BUTTON_ARROW_LEFT.check_for_input(self.CHAMPION_SELECT_MOUSE_POS):
                        self.change_champion_index(self.champion_index - CHAMPION_INDEX_OFFSET)

            pygame.display.update()

    def print_buttons(self):
        for button in [self.BUTTON_ARROW_LEFT, self.BUTTON_ARROW_RIGHT, self.BACK_BUTTON, self.NEXT_BUTTON]:
            button.change_color(self.CHAMPION_SELECT_MOUSE_POS)
            button.update(self.screen)
