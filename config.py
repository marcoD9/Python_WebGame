import random
import pygame
pygame.font.init()
WIDTH, HEIGHT = 640, 360   # Window sizes
FPS = 60

# Ground position and size
GROUND_HEIGHT = 100 
GROUND_Y = HEIGHT- GROUND_HEIGHT
GROUND_X = 0

FONT = pygame.font.SysFont("courier", 20) 

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


# Player 
PLAYER_HEIGHT = 70
PLAYER_WIDTH = 55
PLAYER_VEL = 3
PLAYER_X = WIDTH/2
PLAYER_Y = HEIGHT-PLAYER_HEIGHT-GROUND_HEIGHT
# Jump Variables
ASC_VEL = 5  # Speed while jumping
DESC_VEL =  6 # Speed while falling
JUMP_HEIGHT = 120 # Max jump height

# Attacks
ATTACK_WIDTH = 25
ATTACK_HEIGHT = 25
MAX_ATTACKS = 3
ATTACKS_VEL = 5 

# Enemies
ENEMY_HEIGHT = 60
ENEMY_WIDTH = 50
ENEMY_VEL = random.randint(3,7) # Value between 3 and 7
ENEMY_LIMIT = 2
ENEMY_X_POSITION = WIDTH + 10  
ENEMY_Y_POSITION = HEIGHT - GROUND_HEIGHT - ENEMY_HEIGHT   # Fixed spawn position 
ENEMY_HEALTH = random.randint(5,10)











