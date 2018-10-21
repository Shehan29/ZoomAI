import time
import pygame
import resources.GameUtils as GameUtils


def game_loop():
    pygame.init()
    GameUtils.gameDisplay, GameUtils.traffic_images, GameUtils.car_image = GameUtils.initialize_resources()
    high_score = 0

    while True:
        car, traffic_objects = GameUtils.initialize_traffic()
        dodged = 0

        while True:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                car.go_left()
            if keys[pygame.K_RIGHT]:
                car.go_right()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            GameUtils.gameDisplay.fill(GameUtils.black)
            traffic_objects.lines += car.speed + 15

            GameUtils.draw_traffic(traffic_objects.x, traffic_objects.y, traffic_objects.lines, traffic_objects.curr_vehicle)
            traffic_objects.y += car.speed
            GameUtils.display_car(car.x, car.y)
            GameUtils.display_score(dodged)
            GameUtils.display_high_score(high_score)

            if traffic_objects.y > GameUtils.display_height:
                traffic_objects.update_state()
                dodged += 1
                car.speed += 0.15

            if traffic_objects.lines > 0:
                traffic_objects.lines = -GameUtils.display_height

            if car.crashed(traffic_objects):
                GameUtils.message_display("CRASH")
                if dodged > high_score:
                    high_score = dodged
                time.sleep(1)
                break

            pygame.display.update()


if __name__ == '__main__':
    GameUtils.RENDER = True
    game_loop()
    pygame.quit()
    quit()
