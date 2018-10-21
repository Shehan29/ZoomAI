import random


def random_color():
    levels = range(32, 256, 32)
    return tuple(random.choice(levels) for _ in range(3))


class Vehicle:
    bin = 60

    def __init__(self, display_width, display_height, traffic):
        self.display_width = display_width
        self.display_height = display_height
        self.traffic = traffic
        self.min_obstacle_size = min(traffic, key=lambda t: t[1])[1]
        self.max_obstacle_size = max(traffic, key=lambda t: t[1])[1]
        self.curr_vehicle, self.width, self.height = random.choice(traffic)
        self.y = -self.height
        self.x = random.randrange(0, self.display_width - self.width)

    def get_state(self):
        return {
            "obstacle_x": int(self.x),
            # "obstacle_y": int(self.y),
            # "obstacle_width": self.width,
            # "obstacle_height": self.height
        }

    def get_binned_state(self):
        return {
            "obstacle_x": self.x // self.bin,
            # "obstacle_y": (self.y+self.max_obstacle_size) // self.bin,  # ensure positive value
            # "obstacle_width": self.width // self.bin
        }

    def get_binned_space(self):
        return {
            "obstacle_x": self.display_width // self.bin,
            # "obstacle_x": (self.display_width - self.min_obstacle_size) // self.bin,
            # "obstacle_y": (self.display_height-self.max_obstacle_size) // self.bin,
            # "obstacle_width": (self.max_obstacle_size - self.min_obstacle_size) // self.bin,
        }

    def update_state(self):
        # generate new obstacle with different size and colour
        self.curr_vehicle, self.width, self.height = random.choice(self.traffic)

        # set new obstacle coordinates
        self.y = -self.height
        self.x = random.randrange(0, self.display_width - self.width)
