import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BG_COLOR = (144, 201, 120)

FPS = 60


class LocalWindowPlayerMovement:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.background_color = BG_COLOR
        self.is_running = True

    def draw_background(self):
        self.screen.fill(self.background_color)

    def handle_events(self, move):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    move["moving_left"] = True
                if event.key == pygame.K_d:
                    move["moving_right"] = True
                if event.key == pygame.K_s:
                    move["moving_down"] = True
                if event.key == pygame.K_w:
                    move["moving_up"] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    move["moving_left"] = False
                if event.key == pygame.K_d:
                    move["moving_right"] = False
                if event.key == pygame.K_s:
                    move["moving_down"] = False
                if event.key == pygame.K_w:
                    move["moving_up"] = False
