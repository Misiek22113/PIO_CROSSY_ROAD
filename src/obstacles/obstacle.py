import pygame

OBSTACLE_SCALE = 5

obstacles_types = {  # if _ is first char in obstacle type name, then it's deadly
    "desk": f"obstacles/assets/desk.png",
    "_integral": f"obstacles/assets/integral.png"
}


def create_obstacle(obstacle_type, x, y):
    img_src = obstacles_types.get(obstacle_type, obstacles_types["desk"])
    img = pygame.image.load(img_src)
    scaled_img = pygame.transform.scale(img,
                                        (int(img.get_width() * OBSTACLE_SCALE),
                                         int(img.get_height() * OBSTACLE_SCALE)))
    new_obstacle = Obstacle(scaled_img, x, y)
    if obstacle_type[0] == '_':
        new_obstacle.is_deadly = True

    return new_obstacle


class Obstacle:
    def __init__(self, img, x, y):
        self.x = x
        self.y = y
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)
        self.is_deadly = False

    def print_obstacle(self, screen):
        screen.blit(self.img, self.rect)

    def move_obstacle(self, offset):
        self.x += offset
        self.rect.center = (self.x, self.y)
