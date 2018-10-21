from resources.GameUtils import *
from QTable import *
import pygame


def game_loop(render):
    q_table.q_table = np.load("q_table.npy")

    if render:
        pygame.init()

    for i in range(1, 1000):
        car, obstacle = initialize_objects()
        dodged = 0
        total_reward = 0

        while True:
            curr_state = encode({**car.get_binned_state(), **obstacle.get_binned_state()})

            # execute action
            action = np.argmax(q_table.q_table[curr_state])  # Exploit learned values
            direction = ACTIONS[action]

            if direction == "LEFT":
                car.go_left()
            if direction == "RIGHT":
                car.go_right()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if render:
                        pygame.quit()
                    quit()

            gameDisplay.fill(black)

            obstacle.y += car.speed

            if render:
                draw_obstacle(obstacle.x, obstacle.y, obstacle.width, obstacle.height, obstacle.colour)
                display_car(car.x, car.y)
                display_score(dodged)

            reward = 1

            if obstacle.y > display_height:
                obstacle.update_state()
                dodged += 1
                reward = 10
                car.speed += 0.15

            if car.in_front_of_obstacle(obstacle):
                reward = -10 if car.crashed(obstacle) else -5
            elif action == 1:
                reward = 5

            total_reward += reward

            if car.crashed(obstacle):
                if render:
                    message_display("CRASH")
                break

            if render:
                pygame.display.update()
            # clock.tick(60)

        print("Reward: " + str(total_reward))
        print("Dodged: " + str(dodged))


if __name__ == '__main__':
    game_loop(True)
    pygame.quit()
    quit()

