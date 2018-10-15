import pyautogui
from QTable import *
import sys

DEBUG = True

# Hyper Parameters
alpha = 0.1
gamma = 0.6
epsilon = 0.1

# For plotting metrics
all_epochs = []
all_penalties = []


def train(input_pipe):
    epochs, penalties, reward, = 0, 0, 0

    for i in range(1, 10):
        print("Epoch " + str(i))
        prev_action = 0  # STAY
        dodged = 0

        while True:
            data = input_pipe.recv()
            if data == "QUIT":
                sys.exit()

            reward = 1

            if "CRASH" in data:
                reward = -10
                penalties += 1

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

                if ACTIONS[action] == "LEFT":
                    pyautogui.keyDown('left')
                elif ACTIONS[action] == "RIGHT":
                    pyautogui.keyDown('right')
                else:
                    pyautogui.keyUp('left')
                    pyautogui.keyUp('right')

                print(direction)

    np.save('q_table.npy', q_table.q_table)
