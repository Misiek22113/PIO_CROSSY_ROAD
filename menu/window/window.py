import pygame

pygame.font.init()


class Window:
    BACKGROUND_IMAGE = pygame.image.load("menu/menu_background.png")
    MENU_BUTTON = pygame.image.load("menu/button_menu.png")
    BACKGROUND_IMAGE_POS = (0, 0)
    TEXT_COLOR = (228, 36, 48)
    BASE_COLOR = (249, 154, 40)
    HOVERING_COLOR = (230, 205, 87)
    FONT_HEADER = pygame.font.Font("PressStart2P-Regular.ttf", 80)
    FONT_OPTION = pygame.font.Font("PressStart2P-Regular.ttf", 40)
    FONT_CHAMPION_SELECT = pygame.font.Font("src/menu/PressStart2P-Regular.ttf", 60)
    CHAMPIONS = [[pygame.image.load("src/player/assets/characters/cute_boy/idle/0.png"), "cute boy"],
                 [pygame.image.load("src/player/assets/characters/engineer/idle/0.png"), "engineer"],
                 [pygame.image.load("src/player/assets/characters/frog/idle/0.png"), "frog"],
                 [pygame.image.load("src/player/assets/characters/girl/idle/0.png"), "girl"],
                 [pygame.image.load("src/player/assets/characters/spiderman/idle/0.png"), "spiderman"],
                 [pygame.image.load("src/player/assets/characters/student/idle/0.png"), "student"]]

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
