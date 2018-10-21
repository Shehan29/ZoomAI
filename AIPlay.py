import resources.GameUtils as GameUtils
from QTable import *
import pygame


def game_loop(render):
    GameUtils.gameDisplay, GameUtils.traffic_images, GameUtils.car_image = GameUtils.initialize_resources()
    model = QTable()
    model.q_table = np.load("model.npy")
    high_score = 0
    average_score = 0
    games = 0

    if render:
        pygame.init()

    while True:
        games += 1
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

            if render:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

            traffic_objects.y += car.speed
            traffic_objects.lines += car.speed + 15

            if render:
                GameUtils.gameDisplay.fill(GameUtils.black)
                GameUtils.draw_traffic(traffic_objects.x, traffic_objects.y, traffic_objects.lines, traffic_objects.curr_vehicle)
                GameUtils.display_car(car.x, car.y)
                GameUtils.display_score(dodged)
                GameUtils.display_high_score(high_score)

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
            elif action == 1:
                reward = 5

            total_reward += reward

            if car.crashed(traffic_objects):
                if render:
                    GameUtils.message_display("CRASH")
                if dodged > high_score:
                    high_score = dodged
                break

            if render:
                pygame.display.update()

        print("Game " + str(games))
        print("Reward: " + str(total_reward))
        print("Dodged: " + str(dodged))
        print("High Score: " + str(high_score))
        average_score = average_score*(games-1)/games + dodged/games
        print("Average Score: " + str(average_score))



if __name__ == '__main__':
    render = False
    GameUtils.RENDER = render
    game_loop(render)
    pygame.quit()
    quit()

