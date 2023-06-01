import pygame

OBSTACLE_SCALE = 5

obstacles_types = {
    "desk": f"obstacles/assets/desk.png",
    "_integral": f"obstacles/assets/integral.png"
}


def create_obstacle(obstacle_type, x, y):
    img = obstacles_types.get(obstacle_type, obstacles_types["desk"])
    scaled_img = pygame.transform.scale(img,
                                        (int(img.get_width() * OBSTACLE_SCALE),
                                         int(img.get_height() * OBSTACLE_SCALE)))
    return Obstacle(scaled_img, x, y)


class Obstacle:
    def __init__(self, img, x, y):
        self.x = x
        self.y = y
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)
        self.is_deadly = False

    def print_obstacle(self, screen, offset):
        assert offset <= 0, "Offset must me less than or equal to zero."
        screen.blit(self.img, self.rect + offset)
