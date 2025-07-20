import pygame
import os
from config import ATTACKS_VEL, ATTACK_WIDTH, ATTACK_HEIGHT

FIREBALL_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'FireBall.png')),(ATTACK_WIDTH,ATTACK_HEIGHT))

attacks = []


class Attack:
    def __init__(self, x, y):
     self.x = x
     self.y = y
     self.width = ATTACK_WIDTH
     self.height = ATTACK_HEIGHT
     self.image = FIREBALL_IMAGE 

    def move(self): # Move the projectile
        self.x += ATTACKS_VEL

    def draw(self, surface): # Draw the projectile
        surface.blit(self.image, (self.x, self.y))
       

