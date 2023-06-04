import sys
import pygame
from src.menu.button.button import Button
from src.menu.window.window import Window

EMPTY_BUTTON = None


class Notification(Window):

    def __init__(self, width, height, name, notification_text, return_screen):
        self.WIDTH = width
        self.HEIGHT = height
        self.notification_text = notification_text
        self.OK_BUTTON = EMPTY_BUTTON
        self.NOTIFICATION_MOUSE_POS = EMPTY_BUTTON
        self.return_screen = return_screen
        super().__init__(name, self.WIDTH, self.HEIGHT)

    def print_notification(self):
        self.screen.blit(self.BACKGROUND_IMAGE, self.BACKGROUND_IMAGE_POS)
        self.draw_text(self.notification_text, 640, 300, self.FONT_OPTION, self.TEXT_COLOR)
        self.OK_BUTTON = Button(image=self.MENU_BUTTON, pos=(640, 650), text_input="OK", font=self.FONT_OPTION,
                                base_color=self.BASE_COLOR, hovering_color=self.HOVERING_COLOR)

    def handle_notification_loop(self):
        while True:
            self.print_notification()

            self.NOTIFICATION_MOUSE_POS = pygame.mouse.get_pos()

            self.OK_BUTTON.change_color(self.NOTIFICATION_MOUSE_POS)
            self.OK_BUTTON.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.OK_BUTTON.check_for_input(self.NOTIFICATION_MOUSE_POS):
                        return self.return_screen
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()