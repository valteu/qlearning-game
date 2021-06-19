import numpy as np
import matplotlib.pyplot as plt
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

EPISODES = 25000
SHOOT_PENALTY = 1
ENEMY_HIT = 25
FRIEND_HIT = 300
epsilon = 0.9
EPS_DECAY = 0.9998 

SHOW_EVERY = 5000
MAX_STEPS = 50
posstate = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
actions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
LEARNING_RATE = 0.1
DISCOUNT = 0.95

rewards = []
x_axis = []

class Enemy:

	def __init__(self, pos):
		self.pos = pos
		self.width = int(WIDTH / 10)
		self.height = int(HEIGHT / 10)
		self.speed = int(HEIGHT / 10)
		self.posstate = pos[1] / 80
	def draw(self, screen):
		x, y = self.pos
		w = self.width
		h = self.height
		pygame.draw.rect(screen, (255, 0, 0), (x, y, w, h))
	def update(self, objects):
		direction = np.random.randint(-1, 2)
		if direction == -1 and int(self.pos[1] - self.speed) >= 0:
			self.pos[1] -= self.speed
		elif direction == 0:
			pass
		elif direction == 1 and int(self.pos[1] + self.speed) <= WIDTH:
			self.pos[1] += self.speed
		self.posstate = self.pos[1] / 80

class Friend:

	def __init__(self, pos):
		self.pos = pos
		self.width = int(WIDTH / 10)
		self.height = int(HEIGHT / 10)
		self.speed = int(HEIGHT / 10)
		self.posstate = pos[1] / 80
	def draw(self, screen):
		x, y = self.pos
		w = self.width
		h = self.height
		pygame.draw.rect(screen, (0, 255, 0), (x, y, w, h))
	def update(self, objects):
		direction = np.random.randint(-1, 2)
		if direction == -1 and int(self.pos[1] - self.speed) >= 0:
			self.pos[1] -= self.speed
		elif direction == 0:
			pass
		elif direction == 1 and int(self.pos[1] + self.speed) <= WIDTH:
			self.pos[1] += self.speed
		self.posstate = self.pos[1] / 80

class Agent:

	def __init__(self, pos):
		self.pos = pos
		self.width = int(WIDTH / 10)
		self.height = int(HEIGHT / 10)
		self.posstate = np.random.randint(0, 10)

	def draw(self, screen):
		self.pos
		x, y = self.pos
		w = self.width
		h = self.height
		pygame.draw.rect(screen, (0, 0, 255), (x, y, w, h))

	def update(self, objects):
		pass

	def shoot(self, objects, actioninput=False):
		if actioninput == False:
			action = np.random.randint(0, 10) #10 actions
		else:
			action = actioninput
		if action == 0:
			target = [600, 0 * HEIGHT / 10]
		elif action == 1:
			target = [600, 1 * HEIGHT / 10]
		elif action == 2:
			target = [600, 2 * HEIGHT / 10]
		elif action == 3:
			target = [600, 3 * HEIGHT / 10]
		elif action == 4:
			target = [600, 4 * HEIGHT / 10]
		elif action == 5:
			target = [600, 5 * HEIGHT / 10]
		elif action == 6:
			target = [600, 6 * HEIGHT / 10]
		elif action == 7:
			target = [600, 7 * HEIGHT / 10]
		elif action == 8:
			target = [600, 8 * HEIGHT / 10]
		elif action == 9:
			target = [600, 9 * HEIGHT / 10]
		global bullet
		startpos = [int(self.pos[0] + self.width / 2), int(HEIGHT / 2)]
		bullet = Bullet(startpos, target)
		objects.append(bullet)

	def __sub__(self, other):
		return (self.posstate-other.posstate)	


class Bullet:

	def __init__(self, pos ,aim):
		self.x, self.y = pos
		self.radius = 20
		self.speed = 50
		self.angle = math.atan2(aim[1] - pos[1], aim[0] - pos[0]) #angle to target in radians
		self.dx = math.cos(self.angle) * self.speed
		self.dy = math.sin(self.angle) * self.speed
		self.cx, self.cy = pos
		self.posstate = -1

	def draw(self, screen):
		r = self.radius
		pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), r)

	def update(self, objects):
		self.cx += self.dx
		self.cy += self.dy
		self.x = int(self.cx)
		self.y = int(self.cy)

		if 600 <= self.x <= 680:
			if 0 < self.y < HEIGHT / 10:
				self.posstate = 0
			elif HEIGHT / 10 < self.y < 2 *  HEIGHT / 10:
				self.posstate = 1
			elif 2 * HEIGHT / 10 < self.y < 3 *  HEIGHT / 10:
				self.posstate = 2
			elif 3 * HEIGHT / 10 < self.y < 4 *  HEIGHT / 10:
				self.posstate = 3
			elif 4 * HEIGHT / 10 < self.y < 5 *  HEIGHT / 10:
				self.posstate = 4
			elif 5 * HEIGHT / 10 < self.y < 6 *  HEIGHT / 10:
				self.posstate = 5
			elif 6 * HEIGHT / 10 < self.y < 7 *  HEIGHT / 10:
				self.posstate = 6
			elif 7 * HEIGHT / 10 < self.y < 8 *  HEIGHT / 10:
				self.posstate = 7
			elif 8 * HEIGHT / 10 < self.y < 9 *  HEIGHT / 10:
				self.posstate = 8
			elif 9 * HEIGHT / 10 < self.y < HEIGHT:
				self.posstate = 9
		# elif self.x > WIDTH:
		# 	objects.remove(bullet)
		# 	BULLET_SHOT = False
		# if 0 <= self.y <= HEIGHT:
		# 	pass
		# else:
		# 	objects.remove(bullet)
		# 	BULLET_SHOT = False

def main(epsilon):
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('ai aim game')
	q_table = {}
	for i in range(-len(posstate), len(posstate)):
		for ii in range(-len(posstate), len(posstate)):
			q_table[(i, ii)] = [np.random.uniform(-5, 0) for i in range(len(actions))]

	show = False
	episode_rewards = []
	for episode in range(EPISODES):
		BULLET_SHOT = False
		enemy = Enemy([600, 240])
		agent = Agent(AGENT_POS)
		friend = Friend([600, 480])
		objects = [friend, enemy, agent]

		if episode % SHOW_EVERY == 0:
			show = True
		else:
			show = False

		episode_reward = 0
		for i in range(MAX_STEPS):
			if BULLET_SHOT == True:
				obs = (int(agent-friend), int(agent-enemy))
			else:
				obs = (np.random.randint(0, 10), np.random.randint(0, 10))
			print("obs: ")
			print(obs)
			if np.random.uniform() > epsilon:
				action = np.argmax(q_table[obs])
			else:
				action = np.random.randint(0, 10)
			if BULLET_SHOT == False:
				agent.shoot(objects, action)
				BULLET_SHOT = True
			for obj in objects:
				obj.update(objects)
			if BULLET_SHOT == True:
				if 0 <= bullet.x <= WIDTH: 
					pass
				else:
					objects.remove(bullet)
					BULLET_SHOT = False
				if 0 <= bullet.y <= HEIGHT:
					pass
				else:
					objects.remove(bullet)
					BULLET_SHOT = False

			if bullet.posstate == enemy.posstate:
				reward = ENEMY_HIT
				print("enemy hit")
			elif bullet.posstate == friend.posstate:
				reward = -FRIEND_HIT
				print("friend hit")
			else:
				reward = -SHOOT_PENALTY
			if BULLET_SHOT == True:
				new_obs = (agent-friend, agent-enemy)
			else:
				new_obs = (np.random.randint(0, 10), np.random.randint(0, 10))
			print("new_obs: ")
			print(new_obs)
			max_future_q = np.max(q_table[new_obs])
			current_q = q_table[obs][action]
			if reward == ENEMY_HIT:
				new_q = ENEMY_HIT
			elif reward == -FRIEND_HIT:
				new_q = -FRIEND_HIT
			else:
				new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
			q_table[obs][action] = new_q


			if show:
				print(episode)
				print(i)
				print("--------------------")
				print("enemy: ", enemy.posstate)
				print("friend: ", friend.posstate)
				print("target: ", action)
				print("reward: ", reward + episode_reward)
				print("=====================")
				last_time = time.perf_counter()
				duration = time.perf_counter() - last_time
				last_time += duration
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						show = False
						pygame.quit()
					
				screen.fill((200, 200, 200))
				for obj in objects:
					obj.draw(screen)
				pygame.display.update()
				pygame.time.delay(100)
				time.sleep(max(0, 1 / 60 - (time.perf_counter() - last_time)))
				sys.stdout.flush()

			episode_reward += reward
			if reward == ENEMY_HIT or reward == -FRIEND_HIT:
				break
		episode_rewards.append(episode_reward)

		epsilon *= EPS_DECAY
	oving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode='valid')
	print(oving_avg)
	for i in range(int(EPISODES)):
		x_axis.append(i)
	
	n = 10

	list2 = [sum(episode_rewards[i:i+n])//n for i in range(0,len(episode_rewards),n)]
	for i in range(0,len(episode_rewards)):
		episode_rewards[i] = list2[i//n]
	plt.plot(x_axis, episode_rewards)
	plt.show()
main(epsilon)
