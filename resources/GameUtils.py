import random

import pygame

from resources.Car import Car
from resources.ObstacleFactory import Obstacle
from resources.Traffic import Vehicle

# display
display_width = 800
display_height = 600

# colours
black = (30, 30, 30)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
teal = (0, 243, 88)

RENDER = True
gameDisplay = None
traffic_images = None
car_image = None


# resources
def initialize_resources():
    display = None
    if RENDER:
        display = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption("Zoom")

    race_car = pygame.image.load("images/race_car.png")
    black_car = pygame.image.load("images/black_car.png")
    blue_truck = pygame.image.load("images/blue_truck.png")
    orange_truck = pygame.image.load("images/orange_truck.png")
    red_car = pygame.image.load("images/red_car.png")
    blue_car = pygame.image.load("images/blue_car.png")
    orange_car = pygame.image.load("images/orange_car.png")
    brown_car = pygame.image.load("images/brown_car.png")
    yellow_car = pygame.image.load("images/yellow_car.png")
    yellow_bus = pygame.image.load("images/yellow_bus.png")
    blue_bus = pygame.image.load("images/blue_bus.png")
    vehicle_images = [black_car, blue_truck, orange_truck, red_car, blue_car, orange_car, brown_car, yellow_car, yellow_bus, blue_bus]
    traffic = [(img, img.get_rect().size[0], img.get_rect().size[1]) for img in vehicle_images]
    return display, traffic, race_car


def initialize_objects():
    return Car(display_width, display_height, 20), Obstacle(display_width, display_height)


def initialize_traffic():
    return Car(display_width, display_height, 20), Vehicle(display_width, display_height, traffic_images)


def display_score(count):
    font = pygame.font.SysFont(None, 40)
    text = font.render("Score " + str(count), True, white)
    gameDisplay.blit(text, (20, 20))


def display_text_top_right(message):
    font = pygame.font.SysFont(None, 40)
    text = font.render(message, True, teal)

    text_rect = text.get_rect()
    text_rect.right = 780
    text_rect.top = 20
    gameDisplay.blit(text, text_rect)


def display_epoch(epoch):
    display_text_top_right("Epoch " + str(epoch))


def display_high_score(score):
    display_text_top_right("High Score: " + str(score))


def display_car(x, y):
    gameDisplay.blit(car_image, (x, y))


def random_color():
    levels = range(32,256,32)
    return tuple(random.choice(levels) for _ in range(3))


def draw_obstacle(x, y, width, height, color):
    pygame.draw.rect(gameDisplay, color, [x, y, width, height])


def draw_traffic(x, y, traffic_y, vehicle):
    for i in range(int(traffic_y), display_height, 150):
        for j in range(97, display_width-100, 100):
            pygame.draw.rect(gameDisplay, yellow, [j, i, 6, 50])
    gameDisplay.blit(vehicle, (x, y))


def text_objects(text, font):
    text_surface = font.render(text, True, red)
    return text_surface, text_surface.get_rect()


def message_display(text):
    large_text = pygame.font.Font('freesansbold.ttf', 115)
    text_surface, text_rect = text_objects(text, large_text)
    text_rect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(text_surface, text_rect)


def crash():
    message_display('You Crashed')


def end_game(output_pipe):
    output_pipe.send("QUIT")
    pygame.quit()
    quit()
