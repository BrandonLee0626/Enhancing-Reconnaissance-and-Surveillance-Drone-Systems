from djitellopy.tello import Tello
import pygame
import numpy as np  

class Drone(Tello):
    def __init__(self):
        super().__init__()
        if self.stream_on():
            self.frame = self.get_frame_read().frame
        else:
            self.frame = np.zeros((720, 920, 3), dtype=np.uint8)

    def motion_control(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.move_up(20)
        if keys[pygame.K_a]:
            self.rotate_counter_clockwise(5)
        if keys[pygame.K_s]:
            self.move_down(20)
        if keys[pygame.K_d]:
            self.rotate_clockwise(5)

        if keys[pygame.K_UP]:
            self.move_forward(20)
        if keys[pygame.K_DOWN]:
            self.move_back(20)
        if keys[pygame.K_LEFT]:
            self.move_left(20)
        if keys[pygame.K_RIGHT]:
            self.move_right(20)

        if keys[pygame.K_RETURN]:
            self.land()

    def video_show(self, screen):
        while True:
            frame = self.frame
            surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

            screen.blit(surface, (0, 0))
            pygame.display.flip()
