import pyautogui
import time

DEBUG = False


def process_data(input_pipe):
    start = time.time()
    while True:
        data = input_pipe.recv()
        # print(data)
        if data == "QUIT":
            break
        elif data == "CRASH":
            start = time.time()
        elif isinstance(data, dict):
            pyautogui.keyUp('left')
            pyautogui.keyUp('right')

            if DEBUG:
                print(data['time']-start)

            if (data['car_x'] + 60) > data['obstacle_x']:
                if data['car_x'] < (data['obstacle_x'] + data['obstacle_width']):
                    # print(data)
                    if data['car_x'] > 500:
                        pyautogui.keyDown('left')
                        if DEBUG:
                            print("LEFT")
                    else:
                        pyautogui.keyDown('right')
                        if DEBUG:
                            print("RIGHT")

            if time.time() - data['time'] > 0.5:
                if DEBUG:
                    print("LAG")
