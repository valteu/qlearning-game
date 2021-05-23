import numpy as np
import pygame

import time
import sys
import random
import math

pygame.init()
pygame.font.init()

X_DISTANCE = 10

WIDTH = 800
HEIGHT = 800

BULLET_SHOT = False
AGENT_POS = [20, int(HEIGHT / 2 - HEIGHT / 20)]

HM_EPISODES = 50000
MOVE_PENALTY = 1
ENEMY_PENALTY = 300
FOOD_REWARD = 25
epsilon = 0.9
EPS_DECAY = 0.9998 
SHOW_EVERY = 10000
MAX_STEPS = 200

LEARNING_RATE = 0.1
DISCOUNT = 0.95

class Enemy:

	def __init__(self, pos):
		self.pos = pos
		self.width = int(WIDTH / 10)
		self.height = int(HEIGHT / 10)
		self.speed = int(HEIGHT / 10)

	def draw(self, screen):
		x, y = self.pos
		w = self.width
		h = self.height
		pygame.draw.rect(screen, (255, 0, 0), (x, y, w, h))

	def update(self, duration, objects):
		direction = np.random.randint(-1, 2)
		if direction == -1 and int(self.pos[1] - self.speed) >= 0:
			self.pos[1] -= self.speed
		elif direction == 0:
			pass
		elif direction == 1 and int(self.pos[1] + self.speed) <= WIDTH:
			self.pos[1] += self.speed

class Friend:

	def __init__(self, pos):
		self.pos = pos
		self.width = int(WIDTH / 10)
		self.height = int(HEIGHT / 10)
		self.speed = int(HEIGHT / 10)

	def draw(self, screen):
		x, y = self.pos
		w = self.width
		h = self.height
		pygame.draw.rect(screen, (0, 255, 0), (x, y, w, h))

	def update(self, duration, objects):
		direction = np.random.randint(-1, 2)
		if direction == -1 and int(self.pos[1] - self.speed) >= 0:
			self.pos[1] -= self.speed
		elif direction == 0:
			pass
		elif direction == 1 and int(self.pos[1] + self.speed) <= WIDTH:
			self.pos[1] += self.speed

class Agent:

	def __init__(self, pos):
		self.pos = pos
		self.width = int(WIDTH / 10)
		self.height = int(HEIGHT / 10)

	def draw(self, screen):
		self.pos
		x, y = self.pos
		w = self.width
		h = self.height
		pygame.draw.rect(screen, (0, 0, 255), (x, y, w, h))

	def update(self, duration, objects):
		pass

	def shoot(self, aim, objects):
		action = np.random.randint(0, 10) #10 actions
		if action == 0:
			target = [600, HEIGHT / 10]
		elif action == 1:
			target = [600, 2 * HEIGHT / 10]
		elif action == 2:
			target = [600, 3 * HEIGHT / 10]
		elif action == 3:
			target = [600, 4 * HEIGHT / 10]
		elif action == 4:
			target = [600, 5 * HEIGHT / 10]
		elif action == 5:
			target = [600, 6 * HEIGHT / 10]
		elif action == 6:
			target = [600, 7 * HEIGHT / 10]
		elif action == 7:
			target = [600, 8 * HEIGHT / 10]
		elif action == 8:
			target = [600, 9 * HEIGHT / 10]
		elif action == 9:
			target = [600, 10 * HEIGHT / 10]

		global bullet
		startpos = [int(self.pos[0] + self.width / 2), int(HEIGHT / 2)]
		print(startpos)

		bullet = Bullet(startpos, target)
		objects.append(bullet)

class Bullet:

	def __init__(self, pos ,aim):
		self.x, self.y = pos
		self.radius = 20
		self.aim = aim
		self.speed = 50
		self.angle = math.atan2(aim[1] - pos[1], aim[0] - pos[0]) #angle to target in radians
		self.dx = math.cos(self.angle) * self.speed
		self.dy = math.sin(self.angle) * self.speed
		self.cx, self.cy = pos

	def draw(self, screen):
		r = self.radius
		pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), r)

	def update(self, duration, objects):
		self.cx += self.dx
		self.cy += self.dy
		self.x = int(self.cx)
		self.y = int(self.cy)
		if 0 <= self.x <= WIDTH: 
			pass
		else:
			# objects.remove(bullet)
			BULLET_SHOT = False
		if 0 <= self.y <= HEIGHT:
			pass
		else:
			# objects.remove(bullet)
			BULLET_SHOT = False
	
def main():
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('ai aim-predicting game')
	enemy = Enemy([600, 240])
	agent = Agent(AGENT_POS)
	friend = Friend([600, 480])
	objects = [friend, enemy, agent]
	is_clicked = False

	# q_table = {}
	# for i in range(-SIZE+1, SIZE):
	#     for ii in range(-SIZE+1, SIZE):
	#         for iii in range(-SIZE+1, SIZE):
	#                 for iiii in range(-SIZE+1, SIZE):
	#                     q_table[((i, ii), (iii, iiii))] = [np.random.uniform(-5, 0) for i in range(4)]
	show = True
	BULLET_SHOT = False
	while show:
		last_time = time.perf_counter()
		duration = time.perf_counter() - last_time
		last_time += duration

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				show = False
				pygame.quit()
		keys = pygame.key.get_pressed()
		# if keys[pygame.K_SPACE] and BULLET_SHOT == False:
		# 	objects.append(Bullet([600, 300]))
		# 	BULLET_SHOT = True
		click = pygame.mouse.get_pressed()
		if click[0] == 1 and is_clicked == False:
			is_clicked = True
			tupleaim = pygame.mouse.get_pos()
			aim = list(tupleaim)
			agent.shoot(aim, objects)
			BULLET_SHOT = True
			
		if click[0] == 0 and is_clicked == True:
			is_clicked = False

		for obj in objects:
			obj.update(duration, objects)

		screen.fill((200, 200, 200))
		for obj in objects:
			obj.draw(screen)

		pygame.display.update()
		pygame.time.delay(50)
		time.sleep(max(0, 1 / 60 - (time.perf_counter() - last_time)))
		sys.stdout.flush()


main()
