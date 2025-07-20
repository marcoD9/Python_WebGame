import pygame
import os
from config import PLAYER_VEL, JUMP_HEIGHT, ASC_VEL, DESC_VEL, WIDTH, PLAYER_WIDTH, PLAYER_HEIGHT

PLAYER =  pygame.transform.scale(pygame.image.load(os.path.join('assets', 'Player.png')),(PLAYER_WIDTH,PLAYER_HEIGHT)) # Import the image for the player

class Player:
    def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width= width
            self.height = height
            self.initial_jump_y = y # Store the y as initial jump position
            self.jumping = False  
            self.on_ground = True
            self.is_falling = False  # Default values 
            self.image = PLAYER # Assign  the image we imported to self.image
            
           



    def handle_movement(self, keys):
       # Function to move the character if the movement do not exceed the width
        keys = pygame.key.get_pressed()    
        if keys[pygame.K_LEFT] and self.x-PLAYER_VEL >=0:  # Left
                self.x-=PLAYER_VEL
        if keys[pygame.K_RIGHT] and self.x+PLAYER_VEL <=WIDTH-PLAYER_WIDTH: #Right
                self.x += PLAYER_VEL    
          # Jump
        if self.jumping:
            # Keep ascending until player.y reach JUMP_HEIGHT
            if self.is_falling==False and self.y > (self.initial_jump_y - JUMP_HEIGHT):
                self.y -= ASC_VEL 
            else:   # If we are not ascending we are falling
                self.is_falling = True
            if self.is_falling:  # If we are falling increase player.y untill we reach the initial player.y value
                self.y += DESC_VEL
            # Check if the player is on the ground
            if self.y >= self.initial_jump_y:
                self.y = self.initial_jump_y # Stop moving on the y axis
                self.jumping = False              
                self.on_ground = True   
                self.is_falling = False # Setting the values back to default        
    # Allow to jump only when on the ground      
    def start_jump(self):
             if self.on_ground:
                   self.initial_jump_y = self.y # Store the y position when jump starts
                   self.on_ground = False
                   self.jumping= True
                   self.is_falling = False
                  
             
    def draw(self, surface): # Draw the player
        surface.blit(self.image, (self.x, self.y)) # The method accepts the surface, we'll pass WIN and draw self.image       
        
