import random


def random_color():
    levels = range(32,256,32)
    return tuple(random.choice(levels) for _ in range(3))


class Obstacle:
    min_obstacle_size = 100
    max_obstacle_size = 300
    bin = 20

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
            "obstacle_x": int(self.x),
            "obstacle_y": int(self.y),
            "obstacle_width": self.width,
            "obstacle_height": self.height
        }

    def get__binned_state(self):
        return {
            "obstacle_x": self.x // self.bin,
            "obstacle_y": (self.y+self.max_obstacle_size) // self.bin,  # ensure positive value
            "obstacle_width": self.width // self.bin
        }

    def get_space(self):
        return {
            "obstacle_x": (0, self.display_width - self.width),
            "obstacle_y": (-self.max_obstacle_size, self.display_height),
            "obstacle_width": (self.min_obstacle_size, self.max_obstacle_size),
        }

    def get_binned_space(self):
        return {
            "obstacle_x": (self.display_width - self.width) // self.bin,
            "obstacle_y": (self.display_height-self.max_obstacle_size) // self.bin,
            "obstacle_width": (self.max_obstacle_size - self.min_obstacle_size) // self.bin,
        }

    def update_state(self):
        # generate new obstacle with different size and colour
        self.width = random.randrange(self.min_obstacle_size, self.max_obstacle_size)
        self.height = random.randrange(self.min_obstacle_size, self.max_obstacle_size)
        self.colour = random_color()

        # set new obstacle coordinates
        self.y = -self.height
        self.x = random.randrange(0, self.display_width - self.width)
