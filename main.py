import pygame
from menu.Menu import Menu
from pygame.locals import *
from menu.controls.Controls import Controls
from menu.lobby.Lobby import Lobby
from menu.MenuController.MenuController import MenuController

pygame.init()

menu = MenuController()

menu.handle_main_menu_loop()



pygame.quit()
