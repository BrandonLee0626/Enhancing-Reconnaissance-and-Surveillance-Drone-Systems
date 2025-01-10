from djitellopy.tello import Tello
import pygame

class Drone(Tello):
    def __init__(self):
        super().__init__()
        self.available = False

    def keyborad_motion_control(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.move_up(50)
        if keys[pygame.K_a]:
            self.rotate_counter_clockwise(15)
        if keys[pygame.K_s]:
            self.move_down(50)
        if keys[pygame.K_d]:
            self.rotate_clockwise(15)

        if keys[pygame.K_UP]:
            self.move_forward(50)
        if keys[pygame.K_DOWN]:
            self.move_back(50)
        if keys[pygame.K_LEFT]:
            self.move_left(50)
        if keys[pygame.K_RIGHT]:
            self.move_right(50)

        if keys[pygame.K_RETURN]:
            self.land()

    def video_show(self, screen, model):
        while True:
            frame = model(self.get_frame_read().frame)
            surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

            screen.blit(surface, (0, 0))
            pygame.display.flip()
