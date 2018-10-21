import resources.GameUtils as GameUtils
import pygame
from QTable import *
import os.path


def game_loop(render_game):
    GameUtils.gameDisplay, GameUtils.traffic_images, GameUtils.car_image = GameUtils.initialize_resources()

    model = QTable()
    file_name = "model.npy"
    if os.path.isfile(file_name):
        model.q_table = np.load(file_name)

    if render_game:
        pygame.init()

    # Hyper Parameters
    alpha = 0.1
    gamma = 0.6
    epsilon = 0.2

    for epoch in range(1, 30001):
        car, traffic_objects = GameUtils.initialize_traffic()
        dodged = 0
        total_reward = 0

        while True:
            curr_state = encode({**car.get_binned_state(), **traffic_objects.get_binned_state()}, model.feature_encoding)

            # execute action
            if random.uniform(0, 1) < epsilon:
                action = random_action()  # Explore action space
            else:
                action = np.argmax(model.q_table[curr_state])  # Exploit learned values

            direction = ACTIONS[action]

            if direction == "LEFT":
                car.go_left()
            if direction == "RIGHT":
                car.go_right()

            if render_game:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

            traffic_objects.y += car.speed
            traffic_objects.lines += car.speed + 5

            if render_game:
                GameUtils.gameDisplay.fill(GameUtils.black)
                GameUtils.draw_traffic(traffic_objects.x, traffic_objects.y, traffic_objects.lines, traffic_objects.curr_vehicle)
                GameUtils.display_car(car.x, car.y)
                GameUtils.display_score(dodged)
                GameUtils.display_epoch(epoch)

            reward = 1

            if traffic_objects.y > GameUtils.display_height:
                traffic_objects.update_state()
                dodged += 1
                reward = 10
                car.speed += 0.15

            if traffic_objects.lines > 0:
                traffic_objects.lines = -GameUtils.display_height

            if car.in_front_of_obstacle(traffic_objects):
                reward = -10 if car.crashed(traffic_objects) else -5
            elif car.x < 100 and direction == "LEFT":
                reward = -5
            elif car.x > 700 and direction == "RIGHT":
                reward = -5
            elif action == 1:
                reward = 5

            total_reward += reward

            old_value = model.q_table[curr_state, action]
            next_max = np.max(model.q_table[curr_state])

            new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
            model.q_table[curr_state, action] = new_value

            if car.crashed(traffic_objects):
                if render_game:
                    GameUtils.message_display("CRASH")
                break

            if render_game:
                pygame.display.update()

        if epoch % 1000 == 0:
            np.save(file_name, model.q_table)
            epsilon *= 0.95

        print("Epoch " + str(epoch))
        print("Reward: " + str(total_reward))
        print("Dodged: " + str(dodged))


if __name__ == '__main__':
    render = False
    GameUtils.RENDER = render
    game_loop(render)
    pygame.quit()
    quit()

