import random

class Game:
    def __init__(self):
        self.map = [[0 for _ in range(5)] for _ in range(5)]
        self.number_of_players = 0

    def add_player(self):
        self.number_of_players += 1
        while True:
            x = random.randint(0, 4)
            y = random.randint(0, 4)
            if self.map[x][y] == 0:
                self.map[x][y] = self.number_of_players
                break

    def __str__(self):
        string_map = ''
        for x in range(5):
            for z in range(5):
                string_map = ' '.join([string_map, f'{self.map[x][z]} '])
            string_map = ''.join([string_map, '\n'])
        return string_map

game = Game()

game.add_player()

print(game)
