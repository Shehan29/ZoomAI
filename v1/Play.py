import pyautogui
from GameUtils import *
from QTable import *


def play(input_pipe):
    q_table.q_table = np.load("q_table.npy")
    while True:
        data = input_pipe.recv()
        if data == "QUIT":
            break
        elif isinstance(data, dict):
            curr_state = encode(data)
            action = np.argmax(q_table.q_table[curr_state])

            pyautogui.keyUp('left')
            pyautogui.keyUp('right')
            if ACTIONS[action] == "LEFT":
                pyautogui.keyDown('left')
            elif ACTIONS[action] == "RIGHT":
                pyautogui.keyDown('right')
