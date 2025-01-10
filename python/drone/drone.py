from djitellopy.tello import Tello
import pygame

class Drone(Tello):
    def __init__(self):
        super().__init__()
        self.available = False
        self.in_flight = False

    def keyborad_motion_control(self):
        keys = pygame.key.get_pressed()

        if self.in_flight:
            if keys[pygame.K_w]:
                self.move_up(25)
            if keys[pygame.K_a]:
                self.rotate_counter_clockwise(15)
            if keys[pygame.K_s]:
                self.move_down(25)
            if keys[pygame.K_d]:
                self.rotate_clockwise(15)

            if keys[pygame.K_UP]:
                self.move_forward(25)
            if keys[pygame.K_DOWN]:
                self.move_back(25)
            if keys[pygame.K_LEFT]:
                self.move_left(25)
            if keys[pygame.K_RIGHT]:
                self.move_right(25)

            if keys[pygame.K_RETURN]:
                self.land()
                self.in_flight = False

    def video_show(self, screen, model, stop_event):
        while not stop_event.is_set():
            frame = model(self.get_frame_read().frame)
            surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

            screen.blit(surface, (0, 0))
            pygame.display.flip()
