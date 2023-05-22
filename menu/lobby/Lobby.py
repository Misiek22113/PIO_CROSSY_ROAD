import pygame, sys
from menu.window.window import Window
from menu.button.Button import Button


class Lobby(Window):

    def __init__(self, width, height):
        super().__init__("lobby", width, height)
        self.width = width
        self.height = height
        self.BACK_BUTTON = None
        self.EXIT_BUTTON = None
        self.LOBBY_MOUSE_POS = None

    def print_lobby_menu(self):
        self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))
        self.draw_text("LOBBY", 640, 100, self.FONT_HEADER, self.TEXT_COLOR)
        self.BACK_BUTTON = Button(image=self.MENU_BUTTON, pos=(640, 650), text_input="BACK", font=self.FONT_OPTION,
                                  base_color=self.BASE_COLOR, hovering_color=self.HOVERING_COLOR)

    def handle_lobby_loop(self):
        while True:
            self.print_lobby_menu()

            self.LOBBY_MOUSE_POS = pygame.mouse.get_pos()

            self.BACK_BUTTON.change_color(self.LOBBY_MOUSE_POS)
            self.BACK_BUTTON.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.BACK_BUTTON.check_for_input(self.LOBBY_MOUSE_POS):
                        return "back"
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
