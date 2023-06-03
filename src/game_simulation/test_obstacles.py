# class with methods only to test obstacles, i.e. collisions, printing, moving etc.
# TODO move logic behind this to server, when it will accept multiple players in game
import random

from src.obstacles.obstacle import create_obstacle, Obstacle
from src.map.map import SCROLL_SPEED

OBSTACLE_Y_GENERATION_LOWER_BOUND = 250
OBSTACLE_Y_GENERATION_UPPER_BOUND = 700


class TestObstacles:
    def __init__(self):
        self.obstacles = []

    def add_obstacle(self):
        x = 1400
        y = random.randint(OBSTACLE_Y_GENERATION_LOWER_BOUND, OBSTACLE_Y_GENERATION_UPPER_BOUND)
        obstacle = create_obstacle("desk", x, y)
        self.obstacles.append(obstacle)

    def handle_obstacles(self, screen):
        for obst in self.obstacles:
            obst.move_obstacle(-SCROLL_SPEED)
            obst.print_obstacle(screen)
