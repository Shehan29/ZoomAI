import random


def random_color():
    levels = range(32,256,32)
    return tuple(random.choice(levels) for _ in range(3))


class Obstacle:
    min_obstacle_size = 100
    max_obstacle_size = 300

    def __init__(self, display_width, display_height):
        self.display_width = display_width
        self.display_height = display_height
        self.width = random.randrange(self.min_obstacle_size, self.max_obstacle_size)
        self.height = random.randrange(self.min_obstacle_size, self.max_obstacle_size)
        self.colour = random_color()
        self.y = -self.height
        self.x = random.randrange(0, self.display_width - self.width)

    def get_state(self):
        return {
            "obstacle_x": self.x,
            "obstacle_y": self.y,
            "obstacle_width": self.width,
            "obstacle_height": self.height
        }

    def update_state(self):
        # generate new obstacle with different size and colour
        self.width = random.randrange(self.min_obstacle_size, self.max_obstacle_size)
        self.height = random.randrange(self.min_obstacle_size, self.max_obstacle_size)
        self.colour = random_color()

        # set new obstacle coordinates
        self.y = -self.height
        self.x = random.randrange(0, self.display_width - self.width)
