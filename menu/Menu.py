import pygame, sys
from pygame.locals import *
from menu.button.Button import Button
from menu.window.window import Window
from menu.controls.Controls import Controls


class Menu(Window):

    window = {}
    PLAY_BUTTON = {}
    CONTROLS_BUTTON = {}
    EXIT_BUTTON = {}

    def __init__(self, width, height, name="Menu"):
        super().__init__(name, width, height)
        self.width = width
        self.height = height
        self.handle_menu_loop()

    def print_window_menu(self):
        self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))
        self.draw_text("PASS THE EXAM", 640, 100, self.FONT_HEADER, self.TEXT_COLOR)
        self.PLAY_BUTTON = Button(image=self.MENU_BUTTON, pos=(640, 250), text_input="PLAY", font=self.FONT_OPTION,
                                  base_color=self.BASE_COLOR, hovering_color=self.HOVERING_COLOR)
        self.CONTROLS_BUTTON = Button(image=self.MENU_BUTTON, pos=(640, 400), text_input="CONTROLS",
                                      font=self.FONT_OPTION,
                                      base_color=self.BASE_COLOR, hovering_color=self.HOVERING_COLOR)
        self.EXIT_BUTTON = Button(image=self.MENU_BUTTON, pos=(640, 550), text_input="EXIT", font=self.FONT_OPTION,
                                  base_color=self.BASE_COLOR, hovering_color=self.HOVERING_COLOR)

    def handle_menu_loop(self):

        while True:
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            self.print_window_menu()

            for button in [self.PLAY_BUTTON, self.CONTROLS_BUTTON, self.EXIT_BUTTON]:
                button.change_color(MENU_MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.PLAY_BUTTON.check_for_input(MENU_MOUSE_POS):
                        print("play")
                    if self.CONTROLS_BUTTON.check_for_input(MENU_MOUSE_POS):
                        Controls(self.width, self.height).handle_controls_loop()
                    if self.EXIT_BUTTON.check_for_input(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
