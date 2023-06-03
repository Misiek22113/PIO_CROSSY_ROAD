# class with methods only to test obstacles, i.e. collisions, printing, moving etc.
# TODO move logic behind this to server, when it will accept multiple players in game

from src.obstacles.obstacle import create_obstacle, Obstacle
from src.map.map import SCROLL_SPEED


class TestObstacles:
    def __init__(self):
        self.obstacles = []

    def add_obstacle(self):
        obstacle = create_obstacle("desk", 1100, 500)
        self.obstacles.append(obstacle)

    def handle_obstacles(self, screen):
        for obst in self.obstacles:
            obst.move_obstacle(-SCROLL_SPEED)
            obst.print_obstacle(screen)
