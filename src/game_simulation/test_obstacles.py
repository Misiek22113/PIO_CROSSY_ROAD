import random

import numpy as np

from src.obstacles.obstacle import create_obstacle, obstacles_keys_to_be_drawn

Y = 1
X = 0

OBSTACLE_Y_GENERATION_LOWER_BOUND = 250
OBSTACLE_Y_GENERATION_UPPER_BOUND = 700
SCROLL_SPEED = 1
FINISH_LINE_Y_OFFSET = 532.91


class TestObstacles:
    def __init__(self):
        self.obstacles = np.array([])
        self.names = []

    def add_obstacle(self, generate_finish_line=False):
        x = 1400

        if not generate_finish_line:
            y = random.randint(OBSTACLE_Y_GENERATION_LOWER_BOUND, OBSTACLE_Y_GENERATION_UPPER_BOUND)
            drawn_obstacle_type = random.choice(obstacles_keys_to_be_drawn)
            obstacle = create_obstacle(drawn_obstacle_type, x, y)
            self.names.append(drawn_obstacle_type)
        else:
            y = FINISH_LINE_Y_OFFSET
            obstacle = create_obstacle("+finish_line", x, y)
            self.names.append("+finish_line")

        self.obstacles = np.append(self.obstacles, np.array([obstacle]))

    def handle_obstacles(self):
        index = 0
        while index < len(self.obstacles):
            self.obstacles[index].move_obstacle(-SCROLL_SPEED)
            if self.obstacles[index].x < -50:
                self.obstacles = np.delete(self.obstacles, index)
                del self.names[index]
            else:
                index += 1

    def update_obstacles(self, names, xy):
        self.obstacles = []

        for index, name in enumerate(names):
            try:
                if name == "+finish_line":
                    self.obstacles.append(create_obstacle(name, xy[index][X], FINISH_LINE_Y_OFFSET))
                else:
                    self.obstacles.append(create_obstacle(name, xy[index][X], xy[index][Y]))
            except IndexError:
                continue

    def print_obstacles(self, screen):
        for obst in self.obstacles:
            obst.print_obstacle(screen)
