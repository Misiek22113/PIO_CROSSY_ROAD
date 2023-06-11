import random

import numpy as np

from src.obstacles.obstacle import create_obstacle, obstacles_keys_to_be_drawn

FIRST_OBSTACLE = 0
NEXT_OBSTACLE = 1
X_POSITION_TO_DELETE_OBSTACLE = -50

Y = 1
X = 0

GENERATION_OBSTACLE_X = 1400

OBSTACLE_Y_GENERATION_LOWER_BOUND = 250
OBSTACLE_Y_GENERATION_UPPER_BOUND = 700
SCROLL_SPEED = 1
FINISH_LINE_Y_OFFSET = 532.91


class TestObstacles:
    def __init__(self):
        self.obstacles = np.array([])
        self.names = []

    def add_obstacle(self, generate_finish_line=False):

        if not generate_finish_line:
            y = random.randint(OBSTACLE_Y_GENERATION_LOWER_BOUND, OBSTACLE_Y_GENERATION_UPPER_BOUND)

            if y%2 == 0:
                GENERATION_OBSTACLE_Y = random.randint(OBSTACLE_Y_GENERATION_LOWER_BOUND, y)
            else:
                GENERATION_OBSTACLE_Y = random.randint(y, OBSTACLE_Y_GENERATION_UPPER_BOUND)

            random_number = random.randint(0, 1000)

            drawn_obstacle_type = obstacles_keys_to_be_drawn[random_number % len(obstacles_keys_to_be_drawn)]
            obstacle = create_obstacle(drawn_obstacle_type, GENERATION_OBSTACLE_X, GENERATION_OBSTACLE_Y)
            self.names.append(drawn_obstacle_type)
        else:
            y = FINISH_LINE_Y_OFFSET
            obstacle = create_obstacle("+finish_line", GENERATION_OBSTACLE_X, y)
            self.names.append("+finish_line")

        self.obstacles = np.append(self.obstacles, np.array([obstacle]))

    def handle_obstacles(self):
        index = FIRST_OBSTACLE
        while index < len(self.obstacles):
            self.obstacles[index].move_obstacle(-SCROLL_SPEED)
            if self.obstacles[index].x < X_POSITION_TO_DELETE_OBSTACLE:
                self.obstacles = np.delete(self.obstacles, index)
                del self.names[index]
            else:
                index += NEXT_OBSTACLE

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
