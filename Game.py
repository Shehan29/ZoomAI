import pygame
import time
import random
from multiprocessing import Process, Pipe
from AI import process_data
from ObstacleFactory import Obstacle
from Car import Car

pygame.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
brown = (165, 42, 42)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Lets Race")
clock = pygame.time.Clock()

car_image = pygame.image.load("Racecar.png")


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


def game_loop(output_pipe):
    car = Car(display_width, display_height, 8)
    obstacle = Obstacle(display_width, display_height)

    dodged = 0
    game_exit = False
    pipe_update_counter = 0

    while not game_exit:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car.go_left()
        if keys[pygame.K_RIGHT]:
            car.go_right()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game(output_pipe)

        gameDisplay.fill(white)

        draw_obstacle(obstacle.x, obstacle.y, obstacle.width, obstacle.height, obstacle.colour)
        obstacle.y += car.speed
        display_car(car.x, car.y)
        display_score(dodged)

        if obstacle.y > display_height:
            obstacle.update_state()
            dodged += 1
            car.speed += 0.15

        if car.crashed(obstacle):
            message_display("CRASH")
            time.sleep(1)
            output_pipe.send("CRASH")
            game_loop(output_pipe)

        pygame.display.update()
        pipe_update_counter += 1
        if pipe_update_counter == 15:
            pipe_update_counter = 0
            output_pipe.send({**car.get_state(), **obstacle.get_state(), **{"dodged": dodged, "time": time.time()}})
        clock.tick(60)


if __name__ == '__main__':
    input_pipe, output_pipe = Pipe()
    p = Process(target=process_data, args=(input_pipe,))
    p.start()
    game_loop(output_pipe)
    end_game(output_pipe)


# https://pythonprogramming.net/adding-sounds-music-pygame/
