import sys

from drone import Drone
from video import customYOLO
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

    stop_event = threading.Event()

    video_thread = threading.Thread(target=drone.video_show, args=(screen, model, stop_event, ))
    video_thread.start()

    drone.takeoff()
    drone.in_flight = True

    running = True
    while running:
        fps.tick(10)
        if not drone.in_flight:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
        drone.keyborad_motion_control()
        drone.send_rc_control(0, 0, 0, 0)
    
    drone.streamoff()

    stop_event.set()
    video_thread.join()

    pygame.quit()
    sys.exit()
    
else:
    print("Drone is not available Please try again.")