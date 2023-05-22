import pygame
import sys
from menu.button.Button import Button
from menu.window.window import Window


class ChampionSelect(Window):
    def __init__(self, width, height):
        super().__init__("Champion Select", width, height)
        self.BUTTON_ARROW_RIGHT = None
        self.BUTTON_ARROW_LEFT = None
        self.width = width
        self.height = height
        self.BACK_BUTTON = None
        self.CHAMPION_SELECT_MOUSE_POS = None

    def print_champion_select_menu(self):
        self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))
        self.draw_text("Choose your Champion", 640, 100, self.FONT_CHAMPION_SELECT, self.TEXT_COLOR)
        self.BACK_BUTTON = Button(image=self.MENU_BUTTON, pos=(640, 650), text_input="BACK", font=self.FONT_OPTION,
                                  base_color=self.BASE_COLOR, hovering_color=self.HOVERING_COLOR)
        self.BUTTON_ARROW_LEFT = Button(image=None, pos=(400, 400), text_input="<", font=self.FONT_OPTION,
                                        base_color=self.BASE_COLOR, hovering_color=self.HOVERING_COLOR)
        self.BUTTON_ARROW_RIGHT = Button(image=None, pos=(880, 400), text_input=">", font=self.FONT_OPTION,
                                         base_color=self.BASE_COLOR, hovering_color=self.HOVERING_COLOR)

    def handle_champion_select_loop(self):
        while True:
            self.print_champion_select_menu()

            self.CHAMPION_SELECT_MOUSE_POS = pygame.mouse.get_pos()

            for button in self.BUTTON_ARROW_LEFT, self.BUTTON_ARROW_RIGHT, self.BACK_BUTTON:
                button.change_color(self.CHAMPION_SELECT_MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.BACK_BUTTON.check_for_input(self.CHAMPION_SELECT_MOUSE_POS):
                        return "back"
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
