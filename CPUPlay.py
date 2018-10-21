from resources.GameUtils import *
from QTable import *
import pygame


def game_loop(render):
    model = QTable()
    model.q_table = np.load("model.npy")

    if render:
        pygame.init()

    for i in range(1, 1000):
        car, traffic_objects = initialize_traffic()
        dodged = 0
        total_reward = 0

        while True:
            curr_state = encode({**car.get_binned_state(), **traffic_objects.get_binned_state()}, model.feature_encoding)

            # execute action
            action = np.argmax(model.q_table[curr_state])  # Exploit learned values
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

            traffic_objects.y += car.speed
            traffic_objects.lines += car.speed + 15

            if render:
                draw_traffic(traffic_objects.x, traffic_objects.y, traffic_objects.lines, traffic_objects.curr_vehicle)
                display_car(car.x, car.y)
                display_score(dodged)

            reward = 1

            if traffic_objects.y > display_height:
                traffic_objects.update_state()
                dodged += 1
                reward = 10
                car.speed += 0.15

            if traffic_objects.lines > 0:
                traffic_objects.lines = -display_height

            if car.in_front_of_obstacle(traffic_objects):
                reward = -10 if car.crashed(traffic_objects) else -5
            elif action == 1:
                reward = 5

            total_reward += reward

            if car.crashed(traffic_objects):
                if render:
                    message_display("CRASH")
                break

            if render:
                pygame.display.update()

        print("Reward: " + str(total_reward))
        print("Dodged: " + str(dodged))


if __name__ == '__main__':
    game_loop(True)
    pygame.quit()
    quit()

