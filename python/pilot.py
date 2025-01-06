from drone.drone import Drone
from yolo.customYOLO import customYOLO
import pygame
import threading, time

model = customYOLO("../model/yolo/custom_yolov8s.pt")
print("YOLO model available")

print("Connect to Tello wifi")
time.sleep(7)
drone = Drone()
drone.connect()

print(f'The battery of the drone is {drone.get_battery()}%')
drone.available = drone.get_battery() > 10

if drone.available:
    drone.streamon()

    pygame.init()
    screen = pygame.display.set_mode((960, 720))
    fps = pygame.time.Clock()

    frame = drone.get_frame_read().frame
    surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

    screen.blit(surface, (0, 0))
    pygame.display.flip()

    video_thread = threading.Thread(target=drone.video_show, args=(screen, model, ))
    video_thread.start()

    drone.takeoff()

    running = True
    while running:
        fps.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        drone.keyborad_motion_control()
    
    drone.land()

else:
    print("Drone is not available Please try again.")