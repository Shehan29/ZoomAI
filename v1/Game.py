import time
from resources.GameUtils import *
from multiprocessing import Process, Pipe
from v1.AI import process_data
from Train import train
from NeuralNetwork import NeuralNetwork
from v1.Play import play


def game_loop(output_pipe):
    while True:
        car, obstacle = initialize_objects()

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

            gameDisplay.fill(black)

            draw_obstacle(obstacle.x, obstacle.y, obstacle.width, obstacle.height, obstacle.colour)
            obstacle.y += car.speed
            display_car(car.x, car.y)
            display_score(dodged)

            if obstacle.y > display_height:
                obstacle.update_state()
                dodged += 1
                car.speed += 0.15

            if car.crashed(obstacle):
                print("CRASH")
                message_display("CRASH")
                time.sleep(1)
                output_pipe.send({**car.get_state(), **obstacle.get_state(), **{"dodged": dodged, "CRASH": time.time(), "time": time.time()}})
                break

            pygame.display.update()
            pipe_update_counter += 1
            if pipe_update_counter == 15:
                pipe_update_counter = 0
                output_pipe.send({**car.get_state(), **obstacle.get_state(), **{"dodged": dodged, "time": time.time()}})
            clock.tick(60)


if __name__ == '__main__':
    input_pipe, output_pipe = Pipe()
    nn = NeuralNetwork()
    p = Process(target=nn.train, args=(input_pipe,))
    p.start()

    game_loop(output_pipe)
    end_game(output_pipe)


# https://pythonprogramming.net/adding-sounds-music-pygame/
