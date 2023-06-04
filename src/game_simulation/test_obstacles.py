# class with methods only to test obstacles, i.e. collisions, printing, moving etc.
# TODO move logic behind this to server, when it will accept multiple players in game
import random

from src.obstacles.obstacle import create_obstacle, Obstacle

Y = 1
X = 0

OBSTACLE_Y_GENERATION_LOWER_BOUND = 250
OBSTACLE_Y_GENERATION_UPPER_BOUND = 700
SCROLL_SPEED = 4
FINISH_LINE_Y_OFFSET = 532.91


class TestObstacles:
    def __init__(self):
        self.obstacles = []
        self.names = []

    def add_obstacle(self, generate_finish_line=False):
        x = 1400

        if not generate_finish_line:
            y = random.randint(OBSTACLE_Y_GENERATION_LOWER_BOUND, OBSTACLE_Y_GENERATION_UPPER_BOUND)
            obstacle = create_obstacle("desk", x, y)
            self.names.append("desk")
        else:
            y = FINISH_LINE_Y_OFFSET
            obstacle = create_obstacle("+finish_line", x, y)
            self.names.append("+finish_line")

        self.obstacles.append(obstacle)

    def handle_obstacles(self):
        for obst in self.obstacles:
            obst.move_obstacle(-SCROLL_SPEED)

    def update_obstacles(self, names, xy):
        self.obstacles = []

        for index, name in enumerate(names):
            if name == "+finish_line":
                self.obstacles.append(create_obstacle(name, xy[index][X], FINISH_LINE_Y_OFFSET))
            else:
                self.obstacles.append(create_obstacle(name, xy[index][X], xy[index][Y]))

    def print_obstacles(self, screen):
        for obst in self.obstacles:
            obst.print_obstacle(screen)
