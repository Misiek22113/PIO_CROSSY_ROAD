import pygame
import sys
from src.menu.button.Button import Button
from src.menu.window.window import Window

EMPTY_BUTTON = None


class Menu(Window):

    def __init__(self, width, height, name="Menu"):
        super().__init__(name, width, height)
        self.width = width
        self.height = height
        self.PLAY_BUTTON = EMPTY_BUTTON
        self.CONTROLS_BUTTON = EMPTY_BUTTON
        self.EXIT_BUTTON = EMPTY_BUTTON
        self.MENU_MOUSE_POS = EMPTY_BUTTON

    def print_window_menu(self):
        self.screen.blit(self.BACKGROUND_IMAGE, self.BACKGROUND_IMAGE_POS)
        self.draw_text("PASS THE EXAM", 640, 100, self.FONT_HEADER, self.TEXT_COLOR)
        self.PLAY_BUTTON = Button(image=self.MENU_BUTTON, pos=(640, 350), text_input="PLAY", font=self.FONT_OPTION,
                                  base_color=self.BASE_COLOR, hovering_color=self.HOVERING_COLOR)
        self.CONTROLS_BUTTON = Button(image=self.MENU_BUTTON, pos=(640, 500), text_input="CONTROLS",
                                      font=self.FONT_OPTION,
                                      base_color=self.BASE_COLOR, hovering_color=self.HOVERING_COLOR)
        self.EXIT_BUTTON = Button(image=self.MENU_BUTTON, pos=(640, 650), text_input="EXIT", font=self.FONT_OPTION,
                                  base_color=self.BASE_COLOR, hovering_color=self.HOVERING_COLOR)

    def handle_menu_loop(self):
        while True:
            self.print_window_menu()

            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            for button in [self.PLAY_BUTTON, self.CONTROLS_BUTTON, self.EXIT_BUTTON]:
                button.change_color(self.MENU_MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.PLAY_BUTTON.check_for_input(self.MENU_MOUSE_POS):
                        return "play"
                    if self.CONTROLS_BUTTON.check_for_input(self.MENU_MOUSE_POS):
                        return "controls"
                    if self.EXIT_BUTTON.check_for_input(self.MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
