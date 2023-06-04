import pygame
import sys
from src.menu.button.button import Button
from src.menu.window.window import Window

EMPTY_BUTTON = None


class Controls(Window):

    def __init__(self, width, height):
        super().__init__("Controls", width, height)
        scale = 7
        self.width = width
        self.height = height
        self.BACK_BUTTON = EMPTY_BUTTON
        self.EXIT_BUTTON = EMPTY_BUTTON
        self.CONTROLS_MOUSE_POS = pygame.mouse.get_pos()
        self.KEY_W = pygame.image.load("assets/controls/key_w.png")
        self.KEY_S = pygame.image.load("assets/controls/key_s.png")
        self.KEY_A = pygame.image.load("assets/controls/key_a.png")
        self.KEY_D = pygame.image.load("assets/controls/key_d.png")
        self.KEY_W = pygame.transform.scale(self.KEY_W,
                                            (int(self.KEY_W.get_width() * scale), int(self.KEY_W.get_height() * scale)))
        self.KEY_A = pygame.transform.scale(self.KEY_A,
                                            (int(self.KEY_A.get_width() * scale), int(self.KEY_A.get_height() * scale)))
        self.KEY_S = pygame.transform.scale(self.KEY_S,
                                            (int(self.KEY_S.get_width() * scale), int(self.KEY_S.get_height() * scale)))
        self.KEY_D = pygame.transform.scale(self.KEY_D,
                                            (int(self.KEY_D.get_width() * scale), int(self.KEY_D.get_height() * scale)))
        self.KEY_ARROW = pygame.image.load("assets/controls/key_arrow.png")

    def print_controls(self):
        key_rect = self.KEY_W.get_rect(center=(690, 450))
        self.screen.blit(self.KEY_W, key_rect)
        key_rect = self.KEY_A.get_rect(center=(530, 600))
        self.screen.blit(self.KEY_A, key_rect)
        key_rect = self.KEY_S.get_rect(center=(690, 600))
        self.screen.blit(self.KEY_S, key_rect)
        key_rect = self.KEY_D.get_rect(center=(840, 600))
        self.screen.blit(self.KEY_D, key_rect)

    def print_controls_menu(self):
        self.screen.blit(self.BACKGROUND_IMAGE, self.BACKGROUND_IMAGE_POS)
        self.print_controls()
        self.draw_text("CONTROLS", 640, 100, self.FONT_HEADER, self.TEXT_COLOR)
        self.BACK_BUTTON = Button(image=self.MENU_BUTTON, pos=(640, 650), text_input="BACK", font=self.FONT_OPTION,
                                  base_color=self.BASE_COLOR, hovering_color=self.HOVERING_COLOR)

    def handle_controls_loop(self):
        while True:
            self.print_controls_menu()

            self.CONTROLS_MOUSE_POS = pygame.mouse.get_pos()

            self.BACK_BUTTON.change_color(self.CONTROLS_MOUSE_POS)
            self.BACK_BUTTON.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.BACK_BUTTON.check_for_input(self.CONTROLS_MOUSE_POS):
                        return "back"

            pygame.display.update()
