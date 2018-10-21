import resources.GameUtils as GameUtils
import pygame
from QTable import *
import os.path


def game_loop(render):
    file_name = "model.npy"
    if os.path.isfile(file_name):
        q_table.q_table = np.load(file_name)

    if render:
        pygame.init()

    # Hyper Parameters
    alpha = 0.1
    gamma = 0.6
    epsilon = 0.2

    for i in range(1, 10000):
        car, traffic = GameUtils.initialize_traffic()
        dodged = 0
        total_reward = 0

        while True:
            curr_state = encode({**car.get_binned_state(), **traffic.get_binned_state()})

            # execute action
            if random.uniform(0, 1) < epsilon:
                action = random_action()  # Explore action space
            else:
                action = np.argmax(q_table.q_table[curr_state])  # Exploit learned values

            direction = ACTIONS[action]

            if direction == "LEFT":
                car.go_left()
            if direction == "RIGHT":
                car.go_right()

            if render:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

            traffic.y += car.speed

            if render:
                GameUtils.gameDisplay.fill(GameUtils.black)
                GameUtils.draw_traffic(traffic.x, traffic.y, traffic.curr_vehicle)
                GameUtils.display_car(car.x, car.y)
                GameUtils.display_score(dodged)

            reward = 1

            if traffic.y > GameUtils.display_height:
                traffic.update_state()
                dodged += 1
                reward = 10
                car.speed += 0.15

            if car.in_front_of_obstacle(traffic):
                reward = -10 if car.crashed(traffic) else -5
            elif car.x < 100 and direction == "LEFT":
                reward = -5
            elif car.x > 700 and direction == "RIGHT":
                reward = -5
            elif action == 1:
                reward = 5

            total_reward += reward

            old_value = q_table.q_table[curr_state, action]
            next_max = np.max(q_table.q_table[curr_state])

            new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
            q_table.q_table[curr_state, action] = new_value

            if car.crashed(traffic):
                if render:
                    GameUtils.message_display("CRASH")
                break

            if render:
                pygame.display.update()

        if i % 100 == 0:
            np.save('model.npy', q_table.q_table)
            epsilon *= 0.95

        print("Epoch " + str(i))
        print("Reward: " + str(total_reward))
        print("Dodged: " + str(dodged))


if __name__ == '__main__':
    render = False
    GameUtils.RENDER = render
    game_loop(render)
    pygame.quit()
    quit()

