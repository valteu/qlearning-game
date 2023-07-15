# Q learning game

The game consists of the objects "player" (=agent; blue box), "enemy" (red box), "food" (green box) and "wall" (orange box). The "enemy" and the "food" are moving randomly
across the 10 x 10 field and the "player" is learning to catch the food and not to catch the enemy. Every time the "player" moves, a reward of -1 is added to the 
sum of rewards. The contact with the "food" adds 25 to the reward and the contact with the "enemy" decreases the reward by 300. 

The reinforcement learning based ai is learning in 25000 epochs to achive the highest reward.

**Used libraries:**
- numpy
- pickle
- pygame

**Example run:**
![](0001-0658.gif)

**global parameters**
Parameter | Default | Description
----------|--------|----------
SIZE |10|The size of the grid; SIZE² = number of fields
WIDTH |800| Width of the pygame window; WIDTH / SIZE = width of visualized field
HEIGHT |800| Height of the pygame window; HEIGHT / SIZE = height of visualized field
HM_EPISODES |25000| Number of epochs
MOVE_PENALTY | 1 | Punishment the "player" gets every time it moves (reward - MOVE_PENALTY)
ENEMY_PENALTY | 300 | Punishment the "player" gets every time it hits the "enemy" (reward - ENEMY_PENALTY)
FOOD | 25 | Reward the "player" gets every time it hits the "food" (reward + FOOD)
SHOW_EVERY | 5000 | Shows which epochs will be visualized (HM_EPISODES / SHOW_EVERY = number of visualized epochs)
MAX_STEPS | 200 | Maximum number of steps the "player" can move per epoch

**Bugs:**
- "player", "food", "enemy" can spawn on other object

**Checklist:**
- [x] add "walls"
- [x] load "walls" from a customizable map 
- [ ] fix spawning
- [ ] add multiple "enemies"
- [ ] add bullet to "player"
- [ ] add obstacles

Linked tutorial:
https://www.youtube.com/watch?v=G92TF4xYQcU&t=0s
