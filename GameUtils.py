import pygame
import random
from ObstacleFactory import Obstacle
from Car import Car

pygame.init()

# display
display_width = 800
display_height = 600

# colours
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
brown = (165, 42, 42)

# resources
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Lets Race")
clock = pygame.time.Clock()
car_image = pygame.image.load("Racecar.png")


def initialize_objects():
    return Car(display_width, display_height, 15), Obstacle(display_width, display_height)


def display_score(count):
    font = pygame.font.SysFont(None, 40)
    text = font.render("Score " + str(count), True, black)
    gameDisplay.blit(text, (20, 20))


def display_car(x, y):
    gameDisplay.blit(car_image, (x, y))


def random_color():
    levels = range(32,256,32)
    return tuple(random.choice(levels) for _ in range(3))


def draw_obstacle(x, y, width, height, color):
    pygame.draw.rect(gameDisplay, color, [x, y, width, height])


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
