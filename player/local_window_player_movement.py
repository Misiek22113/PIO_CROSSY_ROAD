import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BG_COLOR = (144, 201, 120)

FPS = 60

pygame.init()


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

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False


local_window = LocalWindowPlayerMovement(SCREEN_WIDTH, SCREEN_HEIGHT)

while local_window.is_running:
    local_window.clock.tick(FPS)
    local_window.draw_background()
    local_window.handle_events()
    pygame.display.update()

    # TODO remember to delete this when real main window will be implemented
pygame.quit()
