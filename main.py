import pygame
import time
import random
from config import *
from player import *
from attack import *
from enemy import *
import os
import asyncio

# --- Initialization ---
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Goblin Attack")
clock = pygame.time.Clock()
BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'Background.png')),(WIDTH,HEIGHT))
GROUND = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'Ground.png')),(WIDTH,GROUND_HEIGHT))

# Global variables that will be managed and reset by reset_game_state()
player = None
attacks = []
enemies = []
start_time = time.time()

# Define intro_duration globally
intro_duration = 3

#--------------------Draw function--------------------
def draw(player, score, show_intro):
    WIN.blit(BG, (0, 0))
    time_text = FONT.render(f"Score : {round(score)}", 1 , BLACK)
    WIN.blit(time_text,(10,10))
    WIN.blit(GROUND, (0, HEIGHT-GROUND_HEIGHT))
    player.draw(WIN)
    
    for attack in attacks:
        attack.draw(WIN)
    for enemy in enemies:
        enemy.draw(WIN)
        
    if show_intro == True:
        start_message = FONT.render("Press 'A' to shoot, Space to jump!",1,BLACK)
        WIN.blit(start_message,(WIDTH/2 - start_message.get_width()/2, HEIGHT/2 - start_message.get_height()/2-80)) 

# --- Function to reset the game state ---
def reset_game_state():
    global attacks
    global enemies
    global player
    global start_time
    
    attacks.clear()
    enemies.clear()
    
    player = Player(x=WIDTH/2 - PLAYER_WIDTH/2, y=HEIGHT - GROUND_HEIGHT-PLAYER_HEIGHT, width=PLAYER_WIDTH, height=PLAYER_HEIGHT)
    
    start_time = time.time()
    
    return {
        'score': 0,
        'spawn_timer': 0,
        'spawn_interval': random.randint(30, 120),
        'show_intro': True
    }

#--------------------Main function--------------------
async def main():
    global attacks
    global enemies
    global player
    
    run = True
    is_playing = True 
    
    # Initialize game state for the very first launch
    game_data = reset_game_state()
    score = game_data['score']
    spawn_timer = game_data['spawn_timer']
    spawn_interval = game_data['spawn_interval']
    show_intro = game_data['show_intro']
    
    while run:
        # Event handling for both playing and game over states
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.KEYDOWN:
                if is_playing: # Handle input only when game is active
                    if event.key == pygame.K_SPACE and player.on_ground:
                        player.start_jump()
                    if event.key == pygame.K_a:
                        if len(attacks) < MAX_ATTACKS:
                            attack_x = player.x + player.width
                            attack_y = player.y + player.height / 2 - ATTACK_HEIGHT / 2
                            attack = Attack(attack_x, attack_y)
                            attacks.append(attack)
                else: # Handle input when game is in game over state
                    if event.key == pygame.K_RETURN:
                        game_data = reset_game_state() # Reset all game variables
                        score = game_data['score']
                        spawn_timer = game_data['spawn_timer']
                        spawn_interval = game_data['spawn_interval']
                        show_intro = game_data['show_intro']
                        is_playing = True # Set game to playing state

        if not run: # Exit if QUIT event was detected
            break

        if is_playing: # --- Game is actively running ---
            clock.tick(FPS)
            elapsed_time = time.time() - start_time

            if elapsed_time >= intro_duration:
                show_intro = False

            # --- Game Logic Updates ---
            spawn_timer += 1
            score += 0.01 
            if spawn_timer >= spawn_interval:
                if len(enemies) < ENEMY_LIMIT:
                    enemy = Enemy()
                    enemies.append(enemy)
                spawn_timer = 0
                spawn_interval = random.randint(30, 120)

            keys_pressed = pygame.key.get_pressed()
            player.handle_movement(keys_pressed)
            
            attacks_to_remove = set()
            enemies_to_remove = set()

            # Update attacks and check collisions with enemies
            for attack in attacks:
                attack.move()
                if attack.x > WIDTH:
                    attacks_to_remove.add(attack)
                    continue
                for enemy in enemies:
                    attack_rect = pygame.Rect(attack.x, attack.y, attack.width, attack.height)
                    enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                    if attack_rect.colliderect(enemy_rect):
                        enemy.health -= 1
                        attacks_to_remove.add(attack)
                        if enemy.health <= 0:
                            enemies_to_remove.add(enemy)
                            score += 10
                        break

            # Check for player collision with enemies
            player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
            for enemy in enemies:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                if player_rect.colliderect(enemy_rect):
                    is_playing = False # Player was hit, set game to inactive state
                    break

            for enemy in enemies:
                enemy.move()
                if enemy.x < 0:
                    enemies_to_remove.add(enemy)
                
            attacks = [attack for attack in attacks if attack not in attacks_to_remove]
            enemies = [enemy for enemy in enemies if enemy not in enemies_to_remove]
            
            # --- Drawing and Display Update for active game ---
            draw(player, score, show_intro)
            pygame.display.update()

        else: # --- Game is in game over state (not playing) ---
            # Display game over messages
            lost_text = FONT.render(f"You lost! Your Score : {round(score)}", 1, RED)
            restart_text = FONT.render("Press Enter to start again!", 1, BLACK)

            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2 - 30))
            WIN.blit(restart_text, (WIDTH/2 - restart_text.get_width()/2, HEIGHT/2 - restart_text.get_height()/2 + 30))
            pygame.display.update()
        
        await asyncio.sleep(0) # Yield control to the browser's event loop

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())