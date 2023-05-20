from menu.Menu import Menu
from menu.controls.Controls import Controls
from menu.lobby.Lobby import Lobby


class MenuController():

    def __init__(self):
        self.menu = Menu(1280, 720)
        self.controls = Controls(1280, 720)
        self.lobby = Lobby(1280, 720)


    def handle_main_menu_loop(self):

        actual = "menu"

        while True:
            if actual == "menu":
                actual = self.menu.handle_menu_loop()
            elif actual == "controls":
                actual = self.controls.handle_controls_loop()
            elif actual == "play":
                actual = self.lobby.handle_lobby_loop()
            elif actual == "back":
                actual = self.menu.handle_menu_loop()

