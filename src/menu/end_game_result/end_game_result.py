import sys
import pygame
from menu.button.Button import Button
from src.menu.window.window import Window

class EndGameResult(Window):

    def __init__(self, name, champion_index, is_win):
        super().__init__(name, 1280, 720)
        self.is_win = is_win
        self.champion_index = champion_index
        self.EXIT_BUTTON = None
        self.MENU_MOUSE_POS = None

    def print_window_end_game_result(self):
        self.screen.blit(self.BACKGROUND_IMAGE, self.BACKGROUND_IMAGE_POS)

        if self.is_win:
            self.draw_text("YOU WIN", 640, 100, self.FONT_HEADER, self.TEXT_COLOR)
        else:
            self.draw_text("YOU LOSE", 640, 100, self.FONT_HEADER, self.TEXT_COLOR)

        self.EXIT_BUTTON = Button(image=self.MENU_BUTTON, pos=(640, 650), text_input="EXIT", font=self.FONT_OPTION,
                                  base_color=self.BASE_COLOR, hovering_color=self.HOVERING_COLOR)

    def draw_player_character(self, x, y):
        scale = 10
        img = self.CHAMPIONS[self.champion_index][0]
        img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
        img_rect = img.get_rect(center=(x, y))
        self.screen.blit(img, img_rect)
        self.draw_text(self.CHAMPIONS[self.champion_index][1], x, 500, self.FONT_OPTION, self.TEXT_COLOR)

    def handle_end_game_result_loop(self):
        while True:
            self.print_window_end_game_result()
            self.draw_player_character(640, 350)

            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            self.EXIT_BUTTON.change_color(self.MENU_MOUSE_POS)
            self.EXIT_BUTTON.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.EXIT_BUTTON.check_for_input(self.MENU_MOUSE_POS):
                        return "menu"


            pygame.display.update()

