from src.menu.Menu import Menu
from src.menu.controls.Controls import Controls
from src.menu.lobby.Lobby import Lobby
from src.menu.champion_select.champion_select import ChampionSelect

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class MenuController:

    def __init__(self):
        self.menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.controls = Controls(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.lobby = Lobby(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.champion_select = ChampionSelect(SCREEN_WIDTH, SCREEN_HEIGHT)

    def handle_main_menu_loop(self, socket, connection):
        actual = "menu"

        while True:
            if actual == "menu" or actual == "back":
                actual, connection = self.menu.handle_menu_loop(socket, connection)

                # Niedźwiedź make communication then.
                if connection == 0:
                    print("Wrong")

                if connection == 1:
                    print("Full")
            elif actual == "controls":
                actual = self.controls.handle_controls_loop()
            elif actual == "play" or actual == "champion_select":
                actual = self.champion_select.handle_champion_select_loop(socket)
            elif actual == "lobby":
                actual = self.lobby.handle_lobby_loop(socket)
