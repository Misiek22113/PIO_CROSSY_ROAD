import pygame

OBSTACLE_SCALE = 5

obstacles_types = {  # if _ is first char in obstacle type name, then it's deadly, if it's +, then that's finish line
    "desk": f"src/obstacles/assets/desk.png",
    "_integral": f"src/obstacles/assets/integral.png",

    "+finish_line": f"src/obstacles/assets/finish_line.png"
}

obstacles_keys = list(obstacles_types.keys())
obstacles_keys_to_be_drawn = obstacles_keys[:-1]


def create_obstacle(obstacle_type, x, y):
    img_src = obstacles_types.get(obstacle_type, obstacles_types["desk"])
    img = pygame.image.load(img_src)

    if obstacle_type != "+finish_line":
        scaled_img = pygame.transform.scale(img,
                                            (int(img.get_width() * OBSTACLE_SCALE),
                                             int(img.get_height() * OBSTACLE_SCALE)))
    else:
        scaled_img = img

    new_obstacle = Obstacle(scaled_img, x, y)
    if obstacle_type[0] == '_':
        new_obstacle.is_deadly = True
    elif obstacle_type[0] == '+':
        new_obstacle.is_finish_line = True

    return new_obstacle


class Obstacle:
    def __init__(self, img, x, y):
        self.x = x
        self.y = y
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)
        self.is_deadly = False
        self.is_finish_line = False

    def print_obstacle(self, screen):
        screen.screen.blit(self.img, self.rect)

    def move_obstacle(self, offset):
        self.x += offset
        self.rect.center = (self.x, self.y)
