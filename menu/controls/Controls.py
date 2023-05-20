import pygame, sys
from pygame.locals import *
from menu.button.Button import Button
# from menu.Menu import Menu
from menu.window.window import Window


class Controls(Window):

    BACK_BUTTON = {}
    EXIT_BUTTON = {}

    def __init__(self, width, height):
        super().__init__("Controls", width, height)
        self.handle_controls_loop()

    def print_controls_menu(self):
        self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))
        self.draw_text("CONTROLS", 640, 100, self.FONT_HEADER, self.TEXT_COLOR)
        self.BACK_BUTTON = Button(image=self.MENU_BUTTON, pos=(640, 650), text_input="BACK", font=self.FONT_OPTION,
                                  base_color=self.BASE_COLOR, hovering_color=self.HOVERING_COLOR)
        self.EXIT_BUTTON = Button(image=self.MENU_BUTTON, pos=(640, 550), text_input="EXIT", font=self.FONT_OPTION,
                                  base_color=self.BASE_COLOR, hovering_color=self.HOVERING_COLOR)

    def handle_controls_loop(self):

        while True:

            CONTROLS_MOUSE_POS = pygame.mouse.get_pos()

            self.print_controls_menu()

            self.BACK_BUTTON.check_for_input(CONTROLS_MOUSE_POS)
            self.BACK_BUTTON.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.BACK_BUTTON.check_for_input(CONTROLS_MOUSE_POS):
                        print("menu")
                    if self.EXIT_BUTTON.check_for_input(CONTROLS_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
