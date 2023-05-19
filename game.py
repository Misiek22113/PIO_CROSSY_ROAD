from __future__ import annotations

import random
import sys
from typing import NoReturn, List

import numpy as np


class Game:
    def __init__(self) -> NoReturn:
        self.map = np.zeros(shape=(5, 5), dtype='int32')
        self.player_numbers = np.array([])
        self.player_positions = []

    def add_player(self, player_number: int, position: List[int, int] = None) -> NoReturn:
        if player_number in self.player_numbers:
            raise ValueError("Player with this number already exists.")

        if not position:
            self.add_random_position(player_number)
        else:
            if self.map[position[0], position[1]] == 0:
                raise ValueError("The position is not empty.")
            else:
                self.map[position[0], position[1]] = player_number

    def add_random_position(self, player_number: int) -> NoReturn:
        while True:
            x = random.randint(0, 4)
            y = random.randint(0, 4)
            if self.map[x][y] == 0:
                self.map[x][y] = player_number
                self.player_positions.append([x, y])
                return

    def __str__(self) -> str:
        map_in_string = ''
        for row in range(5):
            for column in range(5):
                map_in_string = ' '.join([map_in_string, f'{self.map[row, column]} '])
            map_in_string = ''.join([map_in_string, '\n'])
        return map_in_string

    def make_move(self, player_number: int, move: str) -> NoReturn:
        if move == 'w':
            self.go_up(player_number)
        elif move == 's':
            self.go_down(player_number)
        elif move == 'a':
            self.go_left(player_number)
        else:
            self.go_right(player_number)

        return self.player_positions[player_number]

    def go_up(self, player_number):
        if self.player_positions[player_number][0] - 1 >= 0:
            if self.map[self.player_positions[player_number][0] - 1, self.player_positions[player_number][1]] != 0:
                return
            else:
                self.map[self.player_positions[player_number][0], self.player_positions[player_number][1]] = 0
                self.player_positions[player_number][0] -= 1
                self.map[self.player_positions[player_number][0], self.player_positions[player_number][
                    1]] = player_number + 1

    def go_down(self, player_number):
        if self.player_positions[player_number][0] + 1 <= 4:
            if self.map[self.player_positions[player_number][0] + 1, self.player_positions[player_number][1]] != 0:
                return
            else:
                self.map[self.player_positions[player_number][0], self.player_positions[player_number][1]] = 0
                self.player_positions[player_number][0] += 1
                self.map[
                    self.player_positions[player_number][0], self.player_positions[player_number][1]] = player_number + 1

    def go_right(self, player_number):
        if self.player_positions[player_number][1] + 1 < 5:
            if self.map[self.player_positions[player_number][0], self.player_positions[player_number][1] + 1] != 0:
                return
            else:
                self.map[self.player_positions[player_number][0], self.player_positions[player_number][1]] = 0
                self.player_positions[player_number][1] += 1
                self.map[self.player_positions[player_number][0], self.player_positions[player_number][
                    1]] = player_number + 1

    def go_left(self, player_number):
        if self.player_positions[player_number][1] - 1 >= 0:
            if self.map[self.player_positions[player_number][0], self.player_positions[player_number][1] - 1] != 0:
                return
            else:
                self.map[self.player_positions[player_number][0], self.player_positions[player_number][1]] = 0
                self.player_positions[player_number][1] -= 1
                self.map[self.player_positions[player_number][0], self.player_positions[player_number][
                    1]] = player_number + 1


    def actual_position(self, position, player):
        if len(self.player_positions) <= player:
            self.map[position[0], position[1]] = player + 1
            self.player_positions.append(position)
        else:
            self.map[self.player_positions[player][0], self.player_positions[player][1]] = 0
            self.map[position[0], position[1]] = player + 1
            self.player_positions[player] = position

    def get_positions(self):
        return self.player_positions


game = Game()
