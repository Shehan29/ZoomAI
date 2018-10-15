class Car:
    speed_increment = 0.15
    bin = 20

    def __init__(self, display_width, display_height, speed):
        self.display_width = display_width
        self.display_height = display_height
        self.width = 60
        self.x = display_width * 0.48
        self.y = display_height * 0.79
        self.speed = speed
        self.turn_speed = 10

    def get_state(self):
        return {
            "car_x": int(self.x),
            "car_y": int(self.y),
        }

    def get_binned_state(self):
        return {
            "car_x": int(self.x/self.bin)
        }

    def get_binned_space(self):
        return {
            "car_x": (self.display_width - self.width) // self.bin
        }

    def go_faster(self):
        self.speed += self.speed_increment
        self.turn_speed += self.speed_increment

    def go_left(self):
        self.x -= self.turn_speed

    def go_right(self):
        self.x += self.turn_speed

    def hit_wall(self):
        return (self.x > (self.display_width - self.width)) or (self.x < 0)

    def hit_obstacle(self, obstacle):
        tolerance = 20
        if self.y + tolerance < obstacle.y + obstacle.height:
            return ((self.x + self.width) > obstacle.x) and (self.x < (obstacle.x + obstacle.width))
        else:
            return False

    def crashed(self, obstacle):
        return self.hit_wall() or self.hit_obstacle(obstacle)
