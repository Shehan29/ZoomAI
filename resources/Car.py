class Car:
    speed_increment = 0.15
    bin = 50

    def __init__(self, display_width, display_height, speed):
        self.display_width = display_width
        self.display_height = display_height
        self.width = 60
        self.height = 121
        self.x = display_width/2 - self.width/2
        self.y = display_height - (self.height + 5)
        self.speed = speed
        self.turn_speed = speed/1.5

    def get_state(self):
        return {
            "car_x": int(self.x),
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

    def in_front_of_obstacle(self, obstacle):
        return ((self.x + self.width) > obstacle.x) and (self.x < (obstacle.x + obstacle.width))

    def hit_obstacle(self, obstacle):
        tolerance = 28
        if self.y + tolerance < obstacle.y + obstacle.height:
            return self.in_front_of_obstacle(obstacle)
        else:
            return False

    def crashed(self, obstacle):
        return self.hit_wall() or self.hit_obstacle(obstacle)

    def inside_lane(self):
        left = self.x % 100
        return 20 <= left <= 30
