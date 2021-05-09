import pygame

import time
import sys
import random

pygame.init()
pygame.font.init()

SCALE = 40

WIDTH = 800
HEIGHT = 600

class Player:
    def __init__(self, pos):
        self.pos = pos
        self.radius = 1
        self.distance = distance_to_goal(self.pos)[0]
        self.new_distance = WIDTH
        self.weightleft = 1
        self.weightright = 1

    def draw(self, screen):
        x, y = self.pos
        r = self.radius * SCALE
        pygame.draw.circle(screen, (255, 0, 0), (x, y - r), r)

    def update(self, objects, screen):

        direction = "0"
        speed = 5
        objects = objects
        x, y = list(self.pos)

        action = random.uniform(0, 1)
        if action <= ((1/2) * self.weightleft):
            direction = "left"
        elif action <= ((1) * self.weightright):
            direction = "right"
        # elif action <= ((1) * self.weightstand):
        #     direction = "stand"

        if direction == "left":
            x -= speed
        if direction == "right":
            x += speed
        if direction == "stand":
            pass

        self.new_distance = distance_to_goal(self.pos)
        new_distance = int(self.new_distance[0])
        if self.distance < new_distance:
            print("wd")
            if direction == "left":
                self.weightleft = self.weightleft / 1.01

            elif direction == "right":
                self.weightright = self.weightright / 1.01

        elif self.distance > new_distance:
            print("bd")
            if direction == "left":
                self.weightleft = self.weightleft * 1.01

            elif direction == "right":
                self.weightright = self.weightright * 1.01

        self.distance = new_distance
        self.pos[0] = x
            # self.pos[1] = y
        print("l: ", self.weightleft)
        print("r: ", self.weightright)
        if check_collision(objects, self, [x, self.pos[1]]):
            print("goal achieved")

class Goal:
    def __init__(self, pos):
        self.pos = pos
        self.width = 100
        self.height = 600

    def draw(self, screen):
        w = self.width
        h = self.height
        x = self.pos[0] - w
        y = self.pos[1] - h
        pygame.draw.rect(screen, (0, 255, 0), (x, y, w, h))
    def update(self, objects, screen):
        pass

def distance_to_goal(pos):
    posx, posy = pos
    goalx, goaly = goalpos

    xdist = goalx - posx
    ydist = goaly - posy
    distance = [xdist, ydist]

    return distance


def load_level():
    global goalpos
    goalpos = [WIDTH, HEIGHT]
    objects = []
    objects.append(Player([WIDTH/2, HEIGHT]))
    objects.append(Goal(goalpos))
    return objects

def check_collision(objects, mover, probe_pos):
    collisions = []
    for obj in objects:
        if obj is mover:
            continue
        dist_x = obj.pos[0] - probe_pos[0]
        # dist_y = obj.pos[1] - probe_pos[1]
        if probe_pos[0] < mover.pos[0] and dist_x > 0:  #left
            continue
        if probe_pos[0] > mover.pos[0] and dist_x < 0:  #right
            continue
        # if probe_pos[1] < mover.pos[1] and dist_y > 0:  #up
        #     continue
        # if probe_pos[1] > mover.pos[1] and dist_y < 0:  #down
        #     continue
        if abs(dist_x) < 0.95:
            collisions.append(obj)
    return collisions   

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('ai controlled game')
    objects = load_level()
    # player = [obj for obj in objects if isinstance(obj, Player)][0]

    goal = WIDTH

    last_time = time.perf_counter()
    run = True
    while run:
        duration = time.perf_counter() - last_time
        last_time += duration

        # Update
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False       
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run = False

        for obj in objects:
            obj.update(objects, screen)

        # Draw

        screen.fill((200, 200, 100))
        for obj in objects:
            obj.draw(screen)


        pygame.display.update()

        # Wait
        pygame.time.delay(1)
        time.sleep(max(0, 1 / 60 - (time.perf_counter() - last_time)))
        sys.stdout.flush()

    pygame.quit()

main()
