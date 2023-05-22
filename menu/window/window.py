import pygame

pygame.font.init()


class Window:

    BACKGROUND_IMAGE = pygame.image.load("menu/menu_background.png")
    MENU_BUTTON = pygame.image.load("menu/button_menu.png")
    TEXT_COLOR = (228, 36, 48)
    BASE_COLOR = (249, 154, 40)
    HOVERING_COLOR = (230, 205, 87)
    FONT_HEADER = pygame.font.Font("menu/PressStart2P-Regular.ttf", 80)
    FONT_OPTION = pygame.font.Font("menu/PressStart2P-Regular.ttf", 40)
    FONT_CHAMPION_SELECT = pygame.font.Font("menu/PressStart2P-Regular.ttf", 60)

    def __init__(self, name, width, height):
        self.height = height
        self.width = width
        pygame.display.set_caption(name)
        screen_size = (self.width, self.height)
        self.screen = pygame.display.set_mode(screen_size)

    def draw_text(self, text, x, y, font, text_color):
        img = font.render(text, True, text_color)
        img_rect = img.get_rect(center=(x, y))
        self.screen.blit(img, img_rect)
