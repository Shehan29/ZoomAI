import time
from resources.GameUtils import *


def game_loop():
    pygame.init()
    while True:
        car, traffic_objects = initialize_traffic()
        dodged = 0

        while True:
            if car.crashed(traffic_objects):
                time.sleep(1)  # leave CRASH message on screen
                break

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                car.go_left()
            if keys[pygame.K_RIGHT]:
                car.go_right()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            gameDisplay.fill(black)
            traffic_objects.lines += car.speed + 15

            draw_traffic(traffic_objects.x, traffic_objects.y, traffic_objects.lines, traffic_objects.curr_vehicle)
            traffic_objects.y += car.speed
            display_car(car.x, car.y)
            display_score(dodged)

            if traffic_objects.y > display_height:
                traffic_objects.update_state()
                dodged += 1
                car.speed += 0.15

            if traffic_objects.lines > 0:
                traffic_objects.lines = -display_height

            if car.crashed(traffic_objects):
                message_display("CRASH")

            pygame.display.update()


if __name__ == '__main__':
    game_loop()
    pygame.quit()
    quit()
