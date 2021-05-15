import numpy as np
import pygame

import pickle
import time
import sys
import random

pygame.init()
pygame.font.init()

SIZE = 10

WIDTH = 800
HEIGHT = 800

HM_EPISODES = 25000
MOVE_PENALTY = 1
ENEMY_PENALTY = 300
FOOD_REWARD = 25
epsilon = 0.9
EPS_DECAY = 0.9998 
SHOW_EVERY = 5000
MAX_STEPS = 200

start_q_table = None

LEARNING_RATE = 0.1
DISCOUNT = 0.95

class Blob:
    def __init__(self):
        self.x = np.random.randint(0, SIZE)
        self.y = np.random.randint(0, SIZE)
        self.width = int(WIDTH / SIZE)
        self.height = int(HEIGHT / SIZE)

    def __str__(self):
        return f"{self.x}, {self.y}"

    def __sub__(self, other):
        return (self.x-other.x, self.y-other.y)

    def action(self, choice):
        if choice == 0:
            self.move(x=1, y=1)
        elif choice == 1:
            self.move(x=-1, y=-1)
        elif choice == 2:
            self.move(x=-1, y=1)
        elif choice == 3:
            self.move(x=1, y=-1)

    def move(self, x=False, y=False):
     
        if not x:
            probe_x = self.x + np.random.randint(-1, 2)
        else:
            probe_x = self.x + x

        if not y:
            probe_y = self.y + np.random.randint(-1, 2)
        else:
            probe_y = self.y + y


        # If we are out of bounds, fix!
        if self.x < 0:
            self.x = 0
        elif self.x > SIZE-1:
            self.x = SIZE-1
        if self.y < 0:
            self.y = 0
        elif self.y > SIZE-1:
            self.y = SIZE-1

        collision = check_wall_collision(probe_x, probe_y)
        if collision == True:
            pass
        elif collision == False:
            if 0 <= probe_x <= SIZE -1:
                if 0 <= probe_y <= SIZE -1:
                    self.x = probe_x
                    self.y = probe_y

    def draw(self, screen, color):
        w = self.width
        h = self.height
        x = abs(self.x)
        y = abs(self.y)
        pygame.draw.rect(screen, (color), (x * (WIDTH / SIZE), y * (HEIGHT / SIZE), w, h))

class Wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = int(WIDTH / SIZE)
        self.height = int(HEIGHT / SIZE)

    def __str__(self):
        return f"{self.x}, {self.y}"

    def __sub__(self, other):
        return (self.x-other.x, self.y-other.y)

    def draw(self, screen, color):
        w = self.width
        h = self.height
        x = abs(self.x)
        y = abs(self.y)
        pygame.draw.rect(screen, (color), (x * (WIDTH / SIZE), y * (HEIGHT / SIZE), w, h))
 
def check_wall_collision(probe_x, probe_y):
    for obj in walls:
        if obj.x == probe_x:
            if obj.y == probe_y:
                return True
    return False

def load_walls(): 
    global walls  
    map_ = [
        '   #      ',
        '  ###     ',
        '          ',
        '          ',
        '      ##  ',
        '     #  # ',
        '     # ## ',
        '          ',
        ' #        ',
        ' ##       ',
    ]
    walls = []
    y = 0
    for row in map_:
        x = 0
        for cell in row:
            if cell == ' ':
                pass
            if cell =='#':
                walls.append(Wall(x, y))   
            x += 1
        y += 1  
    return walls   

def main(epsilon):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('ai controlled game')
    global walls
    walls = load_walls()
    # player = [obj for obj in objects if isinstance(obj, Player)][0]
    if start_q_table is None:
        q_table = {}
        for i in range(-SIZE+1, SIZE):
            for ii in range(-SIZE+1, SIZE):
                for iii in range(-SIZE+1, SIZE):
                        for iiii in range(-SIZE+1, SIZE):
                            q_table[((i, ii), (iii, iiii))] = [np.random.uniform(-5, 0) for i in range(4)]

    else:
        with open(start_q_table, "rb") as f:
            q_table = pickle.load(f)

    episode_rewards = []

    for episode in range(HM_EPISODES):
        player = Blob()
        food = Blob()
        enemy = Blob()
        objects = [food, enemy, player]
        if episode % SHOW_EVERY == 0:
            print(f"on #{episode}, epsilon is {epsilon}")
            print(f"{SHOW_EVERY} ep mean: {np.mean(episode_rewards[-SHOW_EVERY:])}")
            show = True
        else:
            show = False

        episode_reward = 0
        for i in range(MAX_STEPS):
            obs = (player-food, player-enemy)
            #print(obs)
            if np.random.random() > epsilon:
                # GET THE ACTION
                action = np.argmax(q_table[obs])
            else:
                action = np.random.randint(0, 4)
            # Take the action!
            player.action(action)

            enemy.move()
            food.move()


            if player.x == enemy.x and player.y == enemy.y:
                reward = -ENEMY_PENALTY
            elif player.x == food.x and player.y == food.y:
                reward = FOOD_REWARD
            else:
                reward = -MOVE_PENALTY

            new_obs = (player-food, player-enemy)
            max_future_q = np.max(q_table[new_obs])
            current_q = q_table[obs][action]

            if reward == FOOD_REWARD:
                new_q = FOOD_REWARD
            else:
                new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
            q_table[obs][action] = new_q

            if show:
                epochfont = pygame.font.SysFont(None, 24)
                img = epochfont.render("Epoch: " + str(episode), True, (0, 0, 0))
                rewardfont = pygame.font.SysFont(None, 24)
                img1 = rewardfont.render("Reward: " + str(episode_reward + reward), True, (0, 0, 0))
                last_time = time.perf_counter()
                duration = time.perf_counter() - last_time
                last_time += duration
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    
                screen.fill((200, 200, 200))
                for obj in objects:
                    if obj == enemy:
                        obj.draw(screen, (255, 0, 0))
                    elif obj == food:
                        obj.draw(screen, (0, 255, 0))
                    elif obj == player:
                        obj.draw(screen, (0, 0, 255))
                for obj in walls:
                    obj.draw(screen, (255, 125, 0))
                screen.blit(img, (20, 20))
                screen.blit(img1, (20, 50))

                pygame.display.update()
                pygame.time.delay(50)
                time.sleep(max(0, 1 / 60 - (time.perf_counter() - last_time)))
                sys.stdout.flush()

            episode_reward += reward
            if reward == FOOD_REWARD or reward == -ENEMY_PENALTY:
                break
        episode_rewards.append(episode_reward)
        epsilon *= EPS_DECAY

    oving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode='valid')
    with open(f"qtable-{int(time.time())}.pickle", "wb") as f:
        pickle.dump(q_table, f)

main(epsilon)
