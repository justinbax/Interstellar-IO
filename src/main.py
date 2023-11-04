import math 
import numpy as np
import pygame as pg
from Body import Body
import random
from Camera import Camera
from Spawner import Spawner

DT = 0.5 # Delta time for the physics engine
UPDATES_PER_FRAME = 1 # Number of iterations of the physics engine for each frame

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
NUM_OF_PARTICLES = 25
MIN_ZOOM = 0.1
MAX_ZOOM = 10.0

def main():
    print("interstellarIO")

    pg.init()
    window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pg.display.set_mode(window_size)

    pg.display.set_caption("Interstellar IO")

    screen = pg.display.set_mode(window_size)

    bodies = []

    first_player = Body(2000, np.array([WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2]), np.array([0.0, 0.0]), 0)
    next_player_uid = 1

    bodies.append(first_player)
    
    clock = pg.time.Clock()
    camera = Camera(bodies[0], screen)
    spawner = Spawner(bodies[0])
    
    running = True
    # pygame main loop
    while running:
        screen.fill((255, 255, 255))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                
            if event.type == pg.MOUSEWHEEL:
                sensitivity = 0.1
                print("Camera Zoom:" + str(camera.zoom))
                if camera.zoom + event.y * sensitivity > MIN_ZOOM and camera.zoom + event.y * sensitivity < MAX_ZOOM: 
                    
                    camera.zoom += event.y * sensitivity
        
        for i in range(UPDATES_PER_FRAME):
            for j in bodies:
                 current = 0
            body_count = len(bodies)
            while current < body_count:
                merges = bodies[current].update(DT / UPDATES_PER_FRAME, bodies, current + 1)
                for m in merges:

                    if m[0] == -1:
                        # Self was deleted
                        current -= 1
                    if m[0] == camera.obj.uid:
                        # Camera needs change
                        for b in bodies:
                            if b.uid == m[1]:
                                camera.obj = b
                                break

                body_count -= len(merges)
                current += 1


        n_particles = len(bodies)
        for i in range(NUM_OF_PARTICLES - n_particles):
            bodies.append(spawner.spawnParticle(camera.obj, next_player_uid))
            next_player_uid += 1

        camera.update()
        camera.draw(bodies)
        pg.display.flip()
        clock.tick(60)
    
    pg.quit()

if __name__ == "__main__":
    main()