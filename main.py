import pygame
from menu.Menu import Menu
from pygame.locals import *

menu = Menu(1280, 720)

# temporary game loop

pygame.init()

clock = pygame.time.Clock()
fps = 120
running = True

menu.create_window_menu()

while running:

    menu.print_window_menu()
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    menu.handle_menu_loop()

    pygame.display.update()

pygame.quit()
