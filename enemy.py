import pygame
import os
from config import ENEMY_X_POSITION, ENEMY_Y_POSITION, ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_VEL, ENEMY_HEALTH

ENEMY =  pygame.transform.scale(pygame.image.load(os.path.join('assets', 'Enemy.png')),(ENEMY_WIDTH,ENEMY_HEIGHT))

enemies = []

class Enemy:
    def __init__(self):
        self.x = ENEMY_X_POSITION
        self.y = ENEMY_Y_POSITION
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.health = ENEMY_HEALTH
        self.image = ENEMY


    def move(self):
        self.x -= ENEMY_VEL

    def draw(self, surface): # Draw the enemy
      surface.blit(self.image,(self.x,self.y)) 
