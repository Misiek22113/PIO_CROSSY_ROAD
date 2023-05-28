import pygame
#from player import create_player

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
                
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_a:
            #         player.moving_left = True
            #     if event.key == pygame.K_d:
            #         player.moving_right = True
            #     if event.key == pygame.K_s:
            #         player.moving_down = True
            #     if event.key == pygame.K_w:
            #         player.moving_up = True
            #
            # if event.type == pygame.KEYUP:
            #     if event.key == pygame.K_a:
            #         player.moving_left = False
            #     if event.key == pygame.K_d:
            #         player.moving_right = False
            #     if event.key == pygame.K_s:
            #         player.moving_down = False
            #     if event.key == pygame.K_w:
            #         player.moving_up = False


# local_window = LocalWindowPlayerMovement(SCREEN_WIDTH, SCREEN_HEIGHT)
#
# picked_character = "spiderman"
# player = create_player(100, 100, picked_character)
#
# while local_window.is_running:
#     local_window.clock.tick(FPS)
#     local_window.draw_background()
#     local_window.handle_events()
#
#     player.move()
#     player.print_player(local_window)
#
#     pygame.display.update()
#
#     # TODO remember to delete this when real main window will be implemented
# pygame.quit()
