import pyautogui
from QTable import *
import sys

DEBUG = True


# For plotting metrics
all_epochs = []
all_penalties = []


def train(input_pipe):
    # Hyper Parameters
    alpha = 0.1
    gamma = 0.6
    epsilon = 0.2

    car, obstacle = initialize_objects()  # used to get properties about the objects
    epochs, penalties, reward, = 0, 0, 0

    for i in range(1, 900):
        print("Epoch " + str(i))
        prev_action = 1  # STAY
        dodged = 0

        # start = time.time()

        while True:
            data = input_pipe.recv()

            pyautogui.keyUp('left')
            pyautogui.keyUp('right')


            if data == "QUIT":
                sys.exit()

            reward = -1

            if "CRASH" in data:
                reward = -10
                penalties += 1
            elif ((data['car_x'] + car.width) > data['obstacle_x']) and (data['car_x'] < (data['obstacle_x'] + obstacle.width)):
                reward = -8  # about to hit obstacle
                penalties += 0.1
            elif data['car_x'] < 200 or data['car_x'] < car.display_width-200:
                reward = -5  # discourage going to close to walls
                penalties += 0.01
            elif prev_action == 1:
                reward = 5  # encourage not moving if not in danger

            # get state (result of prev_action)
            curr_state = encode(data)

            if data["dodged"] > dodged:
                dodged = data["dodged"]
                reward = 10

            old_value = q_table.q_table[curr_state, prev_action]
            next_max = np.max(q_table.q_table[curr_state])

            new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
            q_table.q_table[curr_state, prev_action] = new_value

            if "CRASH" in data:
                break
            else:
                # execute action
                if random.uniform(0, 1) < epsilon:
                    action = random_action()  # Explore action space
                else:
                    action = np.argmax(q_table.q_table[curr_state])  # Exploit learned values

                direction = ACTIONS[action]

                # execute action
                if random.uniform(0, 1) < epsilon:
                    action = random_action()  # Explore action space
                else:
                    action = np.argmax(q_table.q_table[curr_state])  # Exploit learned values

                direction = ACTIONS[action]

                if direction == "LEFT":
                    pyautogui.keyDown('left')
                elif direction == "RIGHT":
                    pyautogui.keyDown('right')
                if direction == "LEFT":
                    pyautogui.keyDown('left')
                elif direction == "RIGHT":
                    pyautogui.keyDown('right')

                # remember current action when we get data on the result
                prev_action = action

                # print(direction)

            # if time.time() - data['time'] > 0.5:
            #     if DEBUG:
            #         print("LAG")

        if i % 20 == 0:
            np.save('q_table.npy', q_table.q_table)
            epsilon *= 0.95
