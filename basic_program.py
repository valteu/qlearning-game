import tensorflow as tf
import pygame

import time
import sys

pygame.init()
pygame.font.init()

SCALE = 40

WIDTH = 800
HEIGHT = 600

class Player:
	def __init__(self, pos):
		self.pos = pos
		self.raduis = 1

	def draw(self, screen):
		x, y = self.pos
		r = self.raduis * SCALE
		pygame.draw.circle(screen, (255, 0, 0), (x, y - r), r)

	def update(self, duration, keys, objects, screen):
		collisions = check_collision(objects, self, self.pos)
		speed = 50

		x, y = list(self.pos)
		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
		    x -= speed * duration
		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
		    x += speed * duration
		# if keys[pygame.K_UP] or keys[pygame.K_w]:
		#     y -= speed * duration
		# if keys[pygame.K_DOWN] or keys[pygame.K_s]:
		#     y += speed * duration
		self.pos[0] = x
		# self.pos[1] = y
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

	def update(self, duration, keys, objects, screen):
		pass

def load_level():
	objects = []
	objects.append(Player([WIDTH/2, HEIGHT]))
	objects.append(Goal([WIDTH, HEIGHT]))
	return objects

def check_collision(objects, mover, probe_pos):
    collisions = []
    for obj in objects:
        if obj is mover:
            continue
        dist_x = obj.pos[0] - probe_pos[0]
        dist_y = obj.pos[1] - probe_pos[1]
        if probe_pos[0] < mover.pos[0] and dist_x > 0:  #left
            continue
        if probe_pos[0] > mover.pos[0] and dist_x < 0:  #right
            continue
        # if probe_pos[1] < mover.pos[1] and dist_y > 0:  #up
        #     continue
        # if probe_pos[1] > mover.pos[1] and dist_y < 0:  #down
        #     continue
        if abs(dist_x) < 0.95 and abs(dist_y) < 0.95:
            collisions.append(obj)
    return collisions	


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('ai controlled game')
    objects = load_level()
    # player = [obj for obj in objects if isinstance(obj, Player)][0]

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
        if keys[pygame.K_r]:
            replay()
        for obj in objects:
            obj.update(1 / 60, keys, objects, screen)
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
