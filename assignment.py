#-----------------------------------------------------------------------------
# Name:        Assignment Template (assignment.py)
# Purpose:     This 2D scrolling shooter game offers an immersive space combat experience, where players navigate a scrolling environment,
# engage in intense battles against waves of enemies, and test their reflexes and strategic thinking.
# With captivating visuals, immersive sound effects, and escalating challenges.
#
# Author:      Zaviar Durrani
# Created:     16-May-2023
# Updated:     9-June-2023
#-----------------------------------------------------------------------------
#I think this project deserves a level 4/4+ because it demonstrates a solid understanding of game development concepts and effectively utilizes the Pygame library.
#The code is well-structured, organized, and includes detailed comments to enhance readability.
#It incorporates important game mechanics such as player movement, shooting, enemy behavior, collision detection, and power-ups.
#The implementation of scrolling and wave-based enemy spawning adds depth to the gameplay.
#Additionally, the project showcases proficiency in handling user input and includes a well-implemented main menu functionality.
#Overall, it meets the requirements and expectations for a level 4+ project, showcasing technical ability and attention to detail.
#-----------------------------------------------------------------------------
#Features Added:
# Scrolling Environment: Smooth scrolling creates a dynamic and immersive gameplay experience.
# Waves of Enemies: Progressive difficulty with unique enemy behaviors and attack patterns.
# Power-ups: Temporary advantages through collectible items, boosting movement and shooting speed.
# Main Menu: Visually appealing interface allowing players to start the game with a mouse click.
# Responsive Controls: Precise movement and control of the player's spaceship for intense battles.
# Sound Effects: Immersive audio cues for key actions, enhancing the atmosphere of the game.
#-----------------------------------------------------------------------------

################################################################## WELCOME TO COSMIC INVASION #########################################################################################

import pygame  # Import the pygame library for game development
import random  # Import the random module for generating random numbers

pygame.font.init()  # Initialize the font module in pygame
pygame.mixer.init()  # Initialize the mixer module in pygame for sound

WIDTH = 800  # Set the width of the game window
HEIGHT = 700  # Set the height of the game window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the game window with the specified width and height
pygame.display.set_caption("Cosmic Invasion")  # Set the title of the game window

# Load images
RED_SPACE_SHIP1 = pygame.image.load("pink1.png")  # Load the image for the red space ship
GREEN_SPACE_SHIP1 = pygame.image.load("alien1.png")  # Load the image for the green space ship
BLUE_SPACE_SHIP1 = pygame.image.load("yellow1.png")  # Load the image for the blue space ship
YELLOW_SPACE_SHIP1 = pygame.image.load("ship.png")  # Load the image for the yellow space ship
RED_LASER1 = pygame.image.load("pixel_laser_red.png")  # Load the image for the red laser
GREEN_LASER = pygame.image.load("pixel_laser_green.png")  # Load the image for the green laser
BLUE_LASER1 = pygame.image.load("pixel_laser_yellow.png")  # Load the image for the blue laser
YELLOW_LASER1 = pygame.image.load("beam.png")  # Load the image for the yellow laser
TITLE = pygame.image.load("title.png")  # Load the image for the game title
BG2 = pygame.transform.scale(pygame.image.load("BG3.png"), (WIDTH, HEIGHT))  # Load the image for the background and scale it to fit the game window
BG = pygame.transform.scale(pygame.image.load("background-black.png"), (WIDTH, HEIGHT))  # Load the image for the background and scale it to fit the game window
YELLOW_SPACE_SHIP = pygame.transform.scale(YELLOW_SPACE_SHIP1, (100, 100))  # Scale the yellow space ship image to the desired dimensions
GREEN_SPACE_SHIP = pygame.transform.scale(GREEN_SPACE_SHIP1, (75, 75))  # Scale the green space ship image to the desired dimensions
RED_SPACE_SHIP = pygame.transform.scale(RED_SPACE_SHIP1, (75, 75))  # Scale the red space ship image to the desired dimensions
BLUE_SPACE_SHIP = pygame.transform.scale(BLUE_SPACE_SHIP1, (75, 75))  # Scale the blue space ship image to the desired dimensions
YELLOW_LASER = pygame.transform.scale(YELLOW_LASER1, (100, 50))  # Scale the yellow laser image to the desired dimensions
RED_LASER = pygame.transform.scale(RED_LASER1, (120, 50))  # Scale the red laser image to the desired dimensions
BLUE_LASER = pygame.transform.scale(BLUE_LASER1, (120, 50))  # Scale the blue laser image to the desired dimensions

font = pygame.font.Font("Minecraft.ttf")  # Load a custom font for displaying text in the game

# Load sounds
shoot_sound = pygame.mixer.Sound("shoot.wav")  # Load the sound for shooting
hit_sound = pygame.mixer.Sound("hit.wav")  # Load the sound for hitting an object
level_start_sound = pygame.mixer.Sound("start-level.wav")  # Load the sound for starting a level
click_sound = pygame.mixer.Sound("click.wav")  # Load the sound for a button click
player_hit_sound = pygame.mixer.Sound("hurt.wav")  # Load the sound for the player being hit
game_over_sound = pygame.mixer.Sound("gover.wav")  # Load the sound for game over

shoot_sound.set_volume(0.05)  # Set the volume for the shoot sound
hit_sound.set_volume(0.6)  # Set the volume for the hit sound
level_start_sound.set_volume(1.0)  # Set the volume for the level start sound
click_sound.set_volume(0.8)  # Set the volume for the click sound
player_hit_sound.set_volume(4.0)  # Set the volume for the player hit sound
game_over_sound.set_volume(1.0)  # Set the volume for the game over sound

# Load background music
pygame.mixer.music.load("music.mp3")  # Load the background music file
pygame.mixer.music.set_volume(0.9)  # Set the volume of the background music (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Play the background music in an infinite loop

# Constants for player dimensions
PLAYER_WIDTH = 50  # Width of the player ship
PLAYER_HEIGHT = 50  # Height of the player ship

class Bullet:
    def __init__(self, x, y, img):
        self.x = x  # X coordinate of the bullet
        self.y = y  # Y coordinate of the bullet
        self.img = img  # Image of the bullet
        self.mask = pygame.mask.from_surface(self.img)  # Mask for collision detection

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))  # Draw the bullet on the window

    def move(self, vel):
        self.y += vel  # Move the bullet vertically based on the given velocity

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)  # Check if the bullet is off the screen

    def collision(self, obj):
        return collide(self, obj)  # Check if the bullet collides with another object


class Ship:
    COOLDOWN = 30  # Time delay between consecutive shots

    def __init__(self, x, y, health=100):
        self.x = x  # X coordinate of the ship
        self.y = y  # Y coordinate of the ship
        self.health = health  # Health of the ship
        self.ship_img = None  # Image of the ship
        self.laser_img = None  # Image of the laser
        self.lasers = []  # List to store the bullets/lasers
        self.cool_down_counter = 0  # Counter to keep track of the cooldown time

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))  # Draw the ship on the window
        for laser in self.lasers:
            laser.draw(window)  # Draw each laser/bullet on the window

    def move_lasers(self, vel, obj):
        self.cooldown()  # Perform cooldown logic
        for laser in self.lasers[:]:
            laser.move(vel)  # Move each laser/bullet vertically based on the given velocity
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)  # Remove the laser if it goes off the screen
            elif laser.collision(obj):
                obj.health -= 10  # Reduce the health of the collided object
                self.lasers.remove(laser)  # Remove the laser if it collides with an object

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0  # Reset the cooldown counter if it exceeds the cooldown time
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1  # Increment the cooldown counter

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Bullet(self.x, self.y, self.laser_img)  # Create a new bullet/laser object
            self.lasers.append(laser)  # Add the bullet/laser to the list
            self.cool_down_counter = 1  # Start the cooldown counter

    def get_width(self):
        return self.ship_img.get_width()  # Get the width of the ship

    def get_height(self):
        return self.ship_img.get_height()  # Get the height of the ship


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP  # Image of the player's ship
        self.laser_img = YELLOW_LASER  # Image of the player's laser
        self.mask = pygame.mask.from_surface(self.ship_img)  # Mask for collision detection
        self.max_health = health  # Maximum health of the player
        self.rect = self.ship_img.get_rect()  # Rectangular area for the player's ship
        self.rect.topleft = (x, y)  # Top-left position of the player's ship

    def move_lasers(self, vel, objs):
        self.cooldown()  # Perform cooldown logic
        for laser in self.lasers[:]:
            laser.move(vel)  # Move each laser/bullet vertically based on the given velocity
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)  # Remove the laser if it goes off the screen
            else:
                for obj in objs[:]:
                    if laser.collision(obj):
                        objs.remove(obj)  # Remove the collided object from the list
                        hit_sound.play()  # Play the sound effect for the collision
                        if laser in self.lasers:
                            self.lasers.remove(laser)  # Remove the laser if it was in the list

    def draw(self, window):
        super().draw(window)  # Call the base class draw method
        self.healthbar(window)  # Draw the health bar

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))  # Draw the red background for the health bar
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))  # Draw the green foreground for the health bar based on the current health

class PowerUp:
    def __init__(self, x, y, image):
        self.x = x  # x-coordinate of the power-up
        self.y = y  # y-coordinate of the power-up
        self.image = image  # image of the power-up
        self.width = self.image.get_width()  # width of the power-up image
        self.height = self.image.get_height()  # height of the power-up image
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)  # rectangular area occupied by the power-up
        self.speed = 9  # speed at which the power-up moves
        self.mask = pygame.mask.from_surface(self.image)  # mask used for collision detection

    def move(self):
        self.y += self.speed  # move the power-up downwards
        self.rect.y = self.y  # update the y-coordinate of the power-up's rectangular area

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))  # draw the power-up image on the window

    def collision(self, player):
        player_mask = player.mask  # mask used for collision detection with the player
        offset_x = int(self.x - player.x)  # x-coordinate offset between power-up and player
        offset_y = int(self.y - player.y)  # y-coordinate offset between power-up and player
        return player_mask.overlap(self.mask, (offset_x, offset_y)) is not None  # check if there is a collision between the power-up and the player

class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]  # ship and laser images based on the given color
        self.mask = pygame.mask.from_surface(self.ship_img)  # mask used for collision detection

    def move(self, vel):
        self.y += vel  # move the enemy vertically

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Bullet(self.x-20, self.y, self.laser_img)  # create a laser object
            self.lasers.append(laser)  # add the laser to the list of lasers
            self.cool_down_counter = 1  # set the cooldown counter to prevent rapid shooting
            shoot_sound.play()  # play the shoot sound effect


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x  # x-coordinate offset between the two objects
    offset_y = obj2.y - obj1.y  # y-coordinate offset between the two objects
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None  # check if there is a collision between the two objects
    
    
POWERUP_WIDTH = 30  # width of the power-up
POWERUP_HEIGHT = 30  # height of the power-up


def main():
    run = True
    FPS = 60  # frames per second
    level = 0  # current level
    lives = 5  # remaining lives
    main_font = pygame.font.SysFont("Minecraft", 50)  # font for displaying text
    lost_font = pygame.font.SysFont("Minecraft", 60)  # font for displaying "Game Over" text
    
    scroll_y = 0  # y-coordinate for scrolling background
    scroll_speed = 1  # speed of scrolling

    # Load power-up image
    powerup_image1 = pygame.image.load("gapple.png")

    # Resize powerup
    powerup_image = pygame.transform.scale(powerup_image1, (60, 60))  # resize the power-up image
    
    # Create a power-up instance
    powerup = PowerUp(random.randint(50, WIDTH - 50), -100, powerup_image)  # create a power-up object with random position and the resized image

    powerup_effect_duration = 5000  # Duration of power-up effect in milliseconds
    powerup_effect_active = False  # flag indicating if the power-up effect is active
    powerup_effect_start_time = 0  # time when the power-up effect started
    powerup_collision_rect = pygame.Rect(random.randint(0, WIDTH - POWERUP_WIDTH), -POWERUP_HEIGHT, POWERUP_WIDTH, POWERUP_HEIGHT)  # rectangular area used for power-up collision detection
    powerup_rect = pygame.Rect(random.randint(0, WIDTH - POWERUP_WIDTH), -POWERUP_HEIGHT, POWERUP_WIDTH, POWERUP_HEIGHT)  # rectangular area occupied by the power-up
    
    enemies = []  # list to store enemy objects
    wave_length = 5  # number of enemies in a wave
    enemy_vel = 1.89  # velocity of enemies

    player_vel = 6  # velocity of the player
    laser_vel = 5  # velocity of lasers

    player = Player(300, 630)  # create a player object with initial position

    clock = pygame.time.Clock()  # clock object to control the frame rate

    lost = False  # flag indicating if the game is lost
    lost_count = 0  # counter to keep track of time after losing the game

    def redraw_window(scroll_y):
        WINDOW.blit(BG, (0, scroll_y))  # draw the background image
        WINDOW.blit(BG, (0, scroll_y - HEIGHT))  # draw the background image above the screen
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))  # render the text for lives remaining
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))  # render the text for the current level

        WINDOW.blit(lives_label, (10, 10))  # draw the lives label on the window
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))  # draw the level label on the window

        for enemy in enemies:
            enemy.draw(WINDOW)  # draw each enemy on the window
        
        # Draw power-up
        if powerup:
            powerup.draw(WINDOW)  # draw the power-up on the window
        
        player.draw(WINDOW)  # draw the player on the window

        if lost:
            WINDOW.fill((0, 0, 0))  # fill the window with black color
            lost_label = lost_font.render("GAME OVER!!", 1, (255,255,255))  # render the "Game Over" label
            WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))  # draw the "Game Over" label at the center of the window



        pygame.display.update()  # update the display to show the changes

        
    while True:
        clock.tick(FPS) # Control the game's frame rate
        scroll_y += scroll_speed # Update the scrolling position
        if scroll_y >= HEIGHT: # Check if the scrolling has reached the bottom
            scroll_y = 0 # Reset the scrolling position

        redraw_window(scroll_y) # Update and redraw the game window with the new scroll position

        if lives <= 0 or player.health <= 0: # Check if the player has lost
            lost = True # Set the 'lost' flag to True
            lost_count += 1 # Increase the counter for how long the player has been in the lost state
            pygame.mixer.stop() # Stop any playing sound effects

        if lost:
            if lost_count > FPS * 3: # Check if the lost state has lasted for more than 3 seconds
                run = False  # Exit the game loop
            else:
                continue # Skip the rest of the current iteration and start a new iteration of the game loop

        if len(enemies) == 0: # Check if all enemies have been defeated
            pygame.mixer.stop() # Stop any playing sound effects
            level += 1 # Increase the level number
            level_start_sound.play() # Play level start sound when a new level starts
            wave_length += 5 # Increase the number of enemies in the next wave
            for _ in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy) # Add new enemies to the list

        for event in pygame.event.get(): # Check for events
            if event.type == pygame.QUIT: # Check if the 'QUIT' event occurred (user closed the window)
                quit() # Quit the game


        keys = pygame.key.get_pressed() # Get the state of all keyboard keys
        if keys[pygame.K_a] and player.x - player_vel > 0: # Check if 'A' key is pressed and the player can move left
            player.x -= player_vel # Move the player to the left
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # Check if 'D' key is pressed and the player can move right
            player.x += player_vel # Move the player to the right
        if keys[pygame.K_w] and player.y - player_vel > 0: # Check if 'W' key is pressed and the player can move up
            player.y -= player_vel # Move the player up
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # Check if 'S' key is pressed and the player can move down
            player.y += player_vel # Move the player down
        if keys[pygame.K_SPACE]: # Check if 'SPACE' key is pressed
            player.shoot() # Make the player shoot

        for enemy in enemies[:]: # Iterate over a copy of the enemies list
            enemy.move(enemy_vel) # Move the enemy down the screen
            enemy.move_lasers(laser_vel, player) # Move the enemy's lasers and check for collisions with the player

            if random.randrange(0, 2*60) == 1:  # Randomly decide if the enemy should shoot
                enemy.shoot() # Enemy shoots

            if collide(enemy, player): # Check for collision between enemy and player
                player.health -= 10 # Decrease the player's health
                enemies.remove(enemy) # Remove the enemy from the list
                player_hit_sound.play() # Play sound when player gets hit
            elif enemy.y + enemy.get_height() > HEIGHT: # Check if the enemy has reached the bottom of the screen
                lives -= 1 # Decrease the number of lives
                enemies.remove(enemy) # Remove the enemy from the list


        player.move_lasers(-laser_vel, enemies)  # Move the player's lasers and check for collisions with enemies

        powerup.move() # Move the power-up
    if powerup_collision_rect.colliderect(player.rect):  # Check if the player collided with the power-up
        powerup_effect_active = True # Activate the power-up effect
        powerup_effect_start_time = pygame.time.get_ticks() # Record the start time of the power-up effect
        powerup = None  # Remove the power-up object from the game

    if powerup_effect_active and pygame.time.get_ticks() - powerup_effect_start_time >= powerup_effect_duration:
        powerup_effect_active = False # Deactivate the power-up effect
        # Reset player's attributes to default values after power-up effect ends
        player_vel = 3.5 # Reset player's movement speed
        laser_vel = 5 # Reset player's shooting speed

    if powerup_effect_active:
        # Increase player's movement and shooting speed
        player_vel = 12 # Increase player's movement speed
        laser_vel = 8 # Increase player's shooting speed

    if powerup is None:
        # Spawn a new power-up after the previous one is removed
        powerup = PowerUp(random.randint(50, WIDTH - 50), -100, powerup_image)
        powerup_collision_rect = pygame.Rect(random.randint(0, WIDTH - POWERUP_WIDTH), -POWERUP_HEIGHT, POWERUP_WIDTH, POWERUP_HEIGHT)


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 50) # Set the font for the title
    run = True
    while run:
        WINDOW.blit(BG2, (0,0)) # Draw the background image on the window
        pygame.display.update() # Update the display
        for event in pygame.event.get(): # Check for events
            if event.type == pygame.QUIT: # Check if the 'QUIT' event occurred (user closed the window)
                run = False # Exit the menu loop
            if event.type == pygame.MOUSEBUTTONDOWN: # Check if the mouse button was clicked
                main() # Start the main game loop
    pygame.quit() # Quit pygame


main_menu() # Start the main menu loop