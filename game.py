import pygame
from pygame.locals import *
import time
import random
import subprocess
import sys
# Initialize Pygame
pygame.init()
screen_width, screen_height = 1792, 1024
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Forest Adventure Game")
clock = pygame.time.Clock()

#-------Data---------------
background_image = pygame.image.load("assets/game1_floor.png")
start_sound = pygame.mixer.Sound("assets/startsound.wav")
BGM_fight = pygame.mixer.Sound("assets/music_game.mp3")
gethit = pygame.mixer.Sound("assets/gethit.wav")
monster_gethit = pygame.mixer.Sound("assets/monster_gethit.wav")
win_music = pygame.mixer.Sound("assets/win_music.ogg")
win_image = pygame.image.load("assets/win_picture.png")
jump = pygame.mixer.Sound("assets/jump.wav")
lose_image = pygame.image.load("assets/lose_picture.png")
lose_music = pygame.mixer.Sound("assets/lose_music.wav")
fps = 60
running = True
# Load the sprite sheet image
sprite_sheet_image = pygame.image.load("assets/sword-Sheet.png")
goblin_sheet = pygame.image.load("assets/goblin-Sheet.png")  
slime_sheet = pygame.image.load("assets/slime-Sheet.png")    
wolf_sheet = pygame.image.load("assets/wolf-Sheet.png")
#gem1 = pygame.image.load(("assets/gem1.png"))
#gem2 = pygame.image.load(("assets/gem2.png"))
#gem3 = pygame.image.load(("assets/gem3.png"))
#gem4 = pygame.image.load(("assets/gem4.png"))
#gem5 = pygame.image.load(("assets/gem5.png"))
#gem6 = pygame.image.load(("assets/gem6.png"))
gems = [pygame.image.load(f"assets/gem{i+1}.png") for i in range(6)]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Set the size of each sprite
sprite_width = 32
sprite_height = 32
scale_factor = 3  # Change this factor to scale the size of the character
start_mission_image = pygame.image.load('assets/Start1.png')
#-------Data_End---------------

#-----------Game variables-----------------
gravity = 0.6
character_height = 50
character_width = 25
character_y = screen_height - 64 - character_height  # Starting on the bottom floor
character_x = screen_width // 2 - character_width // 2
player_jump_velocity = -15  # Negative for moving up
jumping = False
velocity_y = 0
velocity_x = 0
speed = 5
all_sprites = pygame.sprite.Group()
pygame.font.init()
font = pygame.font.Font(None, 36)
#-----------Game variables_End-----------------

# Display the start mission image
def display_start_screen():
    screen.blit(start_mission_image, (0, 0))  # Assuming the image size matches the screen size
    pygame.display.flip()
    start_sound.play()
    start_sound.set_volume(0.5)
    time.sleep(1)  # Display the image for 3 seconds
   
# Call the function to display the start mission screen
display_start_screen()
time.sleep(1)
BGM_fight.play(-1)

# Define floors and platforms
floors = [
    pygame.Rect(0, screen_height - 80, screen_width, 80),  # Bottom floor
    pygame.Rect(1200, screen_height - 260, 480, 1),  # 13
    pygame.Rect(1200, screen_height - 460, 380, 1),  # 12
    pygame.Rect(1550, screen_height - 600, 180, 1),  # 11
    pygame.Rect(1200, screen_height - 630, 180, 1),  # 10
    pygame.Rect(1150, screen_height - 930, 180, 1),  # 9
    pygame.Rect(960, screen_height - 760, 200, 1),  # 8
    pygame.Rect(820, screen_height - 620, 140, 1),  # 7
    pygame.Rect(150, screen_height - 780, 160, 1),  # 6
    pygame.Rect(350, screen_height - 600, 260, 1),  # 5
    pygame.Rect(30, screen_height - 520, 280, 1),  # 4
    pygame.Rect(230, screen_height - 400, 280, 1),  #3
    pygame.Rect(430, screen_height - 330, 220, 1),  # 2
    pygame.Rect(500, screen_height - 180, 380, 1),  # 1
]
player_rect = pygame.Rect(character_x, character_y, character_width, character_height)


def check_collisions():
    global jumping, velocity_y
    player_bottom = player_rect.bottom
    if jumping:
        for floor in floors:
            # Check for collision with each floor
            if player_rect.colliderect(floor) and velocity_y > 0:
                player_rect.bottom = floor.top  # Position player on top of the floor
                jumping = False
                velocity_y = 0
                break
def load_and_scale_frames(sheet, frame_width, frame_height, scale_factor):
    """Load frames from a sprite sheet and scale them."""
    frames = []
    sheet_width, sheet_height = sheet.get_width(), sheet.get_height()
    for y in range(0, sheet_height, frame_height):
        for x in range(0, sheet_width, frame_width):
            frame = sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
            scaled_frame = pygame.transform.scale(frame, (int(frame_width * scale_factor), int(frame_height * scale_factor)))
            frames.append(scaled_frame)
    return frames
FRAME_WIDTH, FRAME_HEIGHT = 32, 32
GOBLIN_SCALE, SLIME_SCALE, WOLF_SCALE = 2, 1.5, 2.5  # Different scale factors for each monster

# Constants for frame dimensions (you need to replace these with the actual sizes of your frames)
GOBLIN_FRAME_WIDTH = 32
GOBLIN_FRAME_HEIGHT = 32
SLIME_FRAME_WIDTH = 32
SLIME_FRAME_HEIGHT = 32
WOLF_FRAME_WIDTH = 32
WOLF_FRAME_HEIGHT = 32

goblin_frames = load_and_scale_frames(goblin_sheet, FRAME_WIDTH, FRAME_HEIGHT, GOBLIN_SCALE)
slime_frames = load_and_scale_frames(slime_sheet, FRAME_WIDTH, FRAME_HEIGHT, SLIME_SCALE)
wolf_frames = load_and_scale_frames(wolf_sheet, FRAME_WIDTH, FRAME_HEIGHT, WOLF_SCALE)

# Create a list to store all scaled sprites from the sprite sheet
sprites = []
for i in range(4):  # Assuming there are 4 frames of animation
    sprite = sprite_sheet_image.subsurface((i * sprite_width, 0, sprite_width, sprite_height))
    scaled_sprite = pygame.transform.scale(sprite, (sprite_width * scale_factor, sprite_height * scale_factor))
    sprites.append(scaled_sprite)

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = [pygame.transform.scale(sprite, (sprite_width * scale_factor, sprite_height * scale_factor)) for sprite in sprites]
        self.right_sprites = self.sprites  # Right-facing sprites
        self.left_sprites = [pygame.transform.flip(sprite, True, False) for sprite in self.right_sprites]  # Left-facing sprites
        self.image = self.right_sprites[0]
        self.rect = self.image.get_rect(center=(screen_width // 2, screen_height // 2))
        self.speed = 5
        self.current_frame = 0
        self.animating = False
        self.facing_right = True
        self.attacking = False
        self.health = 300
        self.attack_range = 150
        self.space_pressed = False
        self.attack_timer = 0

    def update(self, keys, monsters):
        self.handle_animation(keys)
        self.move(keys)
        self.check_collision_with_monsters(monsters)

    def handle_animation(self, keys):
        if keys[K_SPACE] and not self.space_pressed:
        
            self.animating = True
            self.space_pressed = True
        elif not keys[K_SPACE]:
            self.space_pressed = False
            self.animating = False

        if self.animating:
            self.current_frame += 1
            if self.current_frame >= len(self.right_sprites):
                self.current_frame = 0
                self.animating = False  # Stop animation after one cycle

        self.image = self.right_sprites[self.current_frame] if self.facing_right else self.left_sprites[self.current_frame]

    def move(self, keys):
        if keys[K_a]:
            self.rect.x -= self.speed
            self.facing_right = False
        if keys[K_d]:
            self.rect.x += self.speed
            self.facing_right = True

    def attack(self, monsters):
        current_time = pygame.time.get_ticks()
        if current_time - self.attack_timer > 500:  # Attack cooldown
            self.attack_timer = current_time
            for monster in monsters:
                # Calculate distance to each monster
                distance = pygame.math.Vector2(self.rect.centerx - monster.rect.centerx,
                                               self.rect.centery - monster.rect.centery).length()
                if distance <= self.attack_range:  # Check if monster is within attack range
                    monster.take_damage(40)  # Damage the monster
                    damage_text = DamageText(40, monster.rect.centerx, monster.rect.centery - 20)
                    all_sprites.add(damage_text)
                    
    def check_collision_with_monsters(self, monsters):
        hits = pygame.sprite.spritecollide(self, monsters, False)
        if hits:
            self.take_damage(1)

    def take_damage(self, amount):
        self.health -= amount
        gethit.play()
        print(f"Player health: {self.health}")
        if self.health <= 0:
            BGM_fight.stop()
            lose_music.play()
            screen.blit(lose_image, (0, 0))
            pygame.display.flip()
            pygame.time.wait(5000)
            pygame.quit()
            subprocess.run(['python', 'menu.py'])
            sys.exit()
            
            

def draw_health_blocks(screen, health):
    for i in range(health // 10):  # Assuming each block represents 10 health points
        pygame.draw.rect(screen, (255, 0, 0), (10 + i * 22, 10, 20, 20))  # Draw health blocks
        
        
class Gem(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        all_sprites.add(self)

class DamageText(pygame.sprite.Sprite):
    def __init__(self, damage, x, y):
        super().__init__()
        self.image = font.render(str(damage), True, (255, 0, 0))  # Create the damage text image
        self.rect = self.image.get_rect(center=(x, y))
        self.counter = 60  # Time till fade
        all_sprites.add(self)

    def update(self, *args, **kwargs):
        # Only self-dependent update logic
        self.rect.y -= 1  # Move text up
        self.counter -= 1
        if self.counter <= 0:
            self.kill()  # Remove text after it's existed long enough
class Monster(pygame.sprite.Sprite):
    def __init__(self, frames, x, y, health=100, attack_range=150):  # Add attack_range with a default value
        super().__init__()
        self.frames = frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_speed = 0.2
        self.animation_index = 0
        self.health = health
        self.attack_range = attack_range  # Store the attack range
        self.contact_timer = 0

    def update(self, player):
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

        # Monster attacks only when touching the player
        if self.rect.colliderect(player.rect):
            self.contact_timer += clock.get_time()
            if self.contact_timer >= 2000:  # Attack every 2 seconds
                player.take_damage(10)
                self.contact_timer = 0

    def take_damage(self, damage):
        self.health -= damage
        DamageText(damage, self.rect.centerx, self.rect.centery)
        monster_gethit.play()
        if self.health <= 0:
            Gem(random.choice(gems), self.rect.centerx, self.rect.centery)
            self.kill()

def spawn_monster_on_floor(monster_class, frames):
    floor = random.choice(floors)  # Select a random floor
    x = random.randint(floor.left, floor.right - int(FRAME_WIDTH * scale_factor))  # Ensure monster stays within the floor
    y = floor.top - int(FRAME_HEIGHT * scale_factor)  # Position the monster exactly on top of the floor
    if x >= floor.right:  # Ensure x is within bounds
        return None
    return monster_class(frames, x, y)

class Goblin(Monster):
    def __init__(self, frames, x, y, health=250, attack_range=10):
        super(Goblin, self).__init__(frames, x, y, health, attack_range)

class Slime(Monster):
    def __init__(self, frames, x, y, health=180, attack_range=10):
        super(Slime, self).__init__(frames, x, y, health, attack_range)

class Wolf(Monster):
    def __init__(self, frames, x, y, health=300, attack_range=10):
        super(Wolf, self).__init__(frames, x, y, health, attack_range)
 
player = Player()
all_sprites = pygame.sprite.Group(player)
font = pygame.font.Font(None, 48)  # Use pygame's default fontd
monsters = pygame.sprite.Group()
for _ in range(5):  # Example count for each type
    monster = spawn_monster_on_floor(Goblin, goblin_frames)
    if monster:
        monsters.add(monster)
    monster = spawn_monster_on_floor(Slime, slime_frames)
    if monster:
        monsters.add(monster)
    monster = spawn_monster_on_floor(Wolf, wolf_frames)
    if monster:
        monsters.add(monster)
        
goblin = Goblin(goblin_frames, x=100, y=100, health=250, attack_range=10)
slime = Slime(slime_frames, x=200, y=200, health=180, attack_range=10)
wolf = Wolf(wolf_frames, x=300, y=300, health=300, attack_range=10)

# Add to the sprite group
monsters.add(goblin, slime, wolf)    
def draw_health_bar(surface, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, (255,0,0), fill_rect)
    pygame.draw.rect(surface, (255,255,255), outline_rect, 2)
    

#Repeating detect function here
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))  # Clear the screen
    # Handle user input
    keys = pygame.key.get_pressed()
    
    # Update the player's animation and movement
    player.update(keys, monsters)
    # Handle player attacks
    if keys[K_SPACE]:
        player.attack(monsters)
        
    # Monster updates
    # Update and draw monsters
    monsters.update(player)
    for monster in monsters:
        if player.rect.colliderect(monster.rect):
            monster.contact_timer += clock.get_time()
            if monster.contact_timer >= 2000:
                player.take_damage(10)
                monster.contact_timer = 0
        else:
            monster.contact_timer = 0

    # Jumping logic
    if keys[K_w] and not jumping:  # If W is pressed and not already jumping
        jumping = True
        jump.play()
        velocity_y = player_jump_velocity

    # Gravity and jumping
    if jumping:
        player.rect.y += velocity_y
        velocity_y += gravity

    # Landing logic
    player_on_ground = False
    for floor in floors:
        if player.rect.colliderect(floor) and velocity_y > 0:
            player.rect.bottom = floor.top  # Land on the floor
            player_on_ground = True
            jumping = False
            velocity_y = 0
            break

    # If player is not colliding with the ground and not jumping, start falling
    if not player_on_ground and not jumping:
        jumping = True

    # Draw everything
    screen.blit(background_image, (0, 0))
    screen.blit(player.image, player.rect)  # Draw the player

    # Draw and update all sprites
    all_sprites.update(keys,monsters) 
    all_sprites.draw(screen)

    # Draw the monsters
    monsters.draw(screen)

    # Draw the player's health bar
    draw_health_blocks(screen, player.health)
    
    if not monsters:  # This checks if the group is empty
        screen.blit(win_image, (0, 0))
        pygame.display.flip()
        win_music.play()
        pygame.time.wait(5000)  # Display the message for 5 seconds before ending the game
        pygame.quit()
        subprocess.run(['python', 'FinalBoss.py'])
        sys.exit()
        

    pygame.display.flip()  # Update the display


pygame.quit()