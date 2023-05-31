import pygame
from src.menu.Menu import Menu
from src.menu.controls.Controls import Controls
from src.menu.lobby.Lobby import Lobby
from src.menu.MenuController.MenuController import MenuController

pygame.display.init()
menu = MenuController()
menu.handle_main_menu_loop()

pygame.quit()
