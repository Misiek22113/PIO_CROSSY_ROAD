import pygame
from src.menu.menu import Menu
from src.menu.controls.controls import Controls
from src.menu.lobby.lobby import Lobby
from src.menu.MenuController.menu_controller import MenuController

pygame.display.init()
menu = MenuController()
menu.handle_main_menu_loop()

pygame.quit()
