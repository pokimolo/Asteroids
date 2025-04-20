import pygame
import math
import time
import random

width = 800
height = 600

z = [width, height]
transparent = (0, 0, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
screen_display = pygame.display
screen_display.set_caption('Asteroids')
surface = screen_display.set_mode(z)

# Ship
ship = pygame.image.load('pictures/spaceship.png').convert_alpha()
P_X = width / 2 - 16  # top-left ship coords
P_Y = height / 2 - 16
heart = pygame.image.load('pictures/heart.png').convert_alpha()

# Background
bg = pygame.image.load('pictures/Bg.jpg')
bg = pygame.transform.scale(bg, (width, height))

################################## SCOREBOARD ###################################
    
def update_scoreboard(hit_asteroids):
    with open('scoreboard.txt', 'r') as file:
        lines = file.readlines()
    new_score = hit_asteroids
    new_name = input('Enter name for scoreboard: ')
    for line in lines:
        line_parts = line.split()
        if len(line_parts) < 2:
            continue
        score = line_parts[1]
        if new_score > int(score):
            new_line = f"{new_name} {new_score}\n"
            lines.insert(lines.index(line), new_line)
            break
    if len(lines) > 5:
        lines.pop()
    with open('scoreboard.txt', 'w') as file:
            file.writelines(lines)
   
def print_board():
    print('##########TOP SCORES##########')
    with open('scoreboard.txt', 'r') as file:
        lines = file.readlines()
    for line in lines:
        print(line)
    print('##############################')

class Laser:
    def __init__(self, angle):
        self.x = width / 2
        self.y = height / 2
        self.angle = angle+90 
        self.speed = 3
        self.length = 10

        rad = math.radians(self.angle)
        self.dx = math.cos(rad) * self.speed
        self.dy = -math.sin(rad) * self.speed

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, surface):
        rad = math.radians(self.angle)
        end_x = self.x + math.cos(rad) * self.length
        end_y = self.y - math.sin(rad) * self.length
        pygame.draw.line(surface, red, (self.x, self.y), (end_x, end_y), 4)


class Asteroid:
    def __init__(self, size, speed, angle):
        self.size = size
        self.speed = speed

        # Position (spawn from edges)
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            self.x = random.randint(0, width)
            self.y = -60
        elif edge == 'bottom':
            self.x = random.randint(0, width)
            self.y = height + 60
        elif edge == 'left':
            self.x = -60
            self.y = random.randint(0, height)
        elif edge == 'right':
            self.x = width + 60
            self.y = random.randint(0, height)


        # Determine angle, 30% of asteroids will not be targeting the ship
        if random.random() < 0.3:
            self.angle = random.randint(0, 360)
        else:
            # Angle toward center of screen
            center_x = width / 2
            center_y = height / 2
            dx = center_x - self.x
            dy = center_y - self.y
            self.angle = math.degrees(math.atan2(-dy, dx))

        # Now calculate velocity based on finalized angle
        rad = math.radians(self.angle)
        self.dx = math.cos(rad) * self.speed
        self.dy = -math.sin(rad) * self.speed

        img_size = self.size * 20
        self.rect = pygame.Rect(self.x, self.y, img_size, img_size)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, surface):
        asteroid = pygame.image.load('pictures/asteroid1.png').convert_alpha()
        asteroid = pygame.transform.scale(asteroid, (self.size * 20, self.size * 20))
        surface.blit(asteroid, (self.x, self.y))
        # Uncomment for debugging
        # pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)

def playing(surface, difficulty):
    pygame.init()
    window = True
    lasers = []
    asteroids = []
    laser_count = 0
    hit_asteroids = 0
    clock = pygame.time.Clock()
    health = 3
    spawn_timer = 0
    #default asteroid speed
    speed = .75
    if difficulty == 1:
        spawn_interval = 30
    elif difficulty == 2:
        spawn_interval = 20
        speed = 1.2
    else:
        spawn_interval = 10
    
    while window and health > 0:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                lasers.append(Laser(angle))
                laser_count += 1
        
        # Draw background
        surface.blit(bg, (0, 0))
        
        # Display hearts
        if health == 3:
            surface.blit(heart, (P_X-12, P_Y-24))
            surface.blit(heart, (P_X+8, P_Y-24))
            surface.blit(heart, (P_X+28, P_Y-24))
        elif health == 2:
            surface.blit(heart, (P_X-12, P_Y-24))
            surface.blit(heart, (P_X+8, P_Y-24))
        elif health == 1:
            surface.blit(heart, (P_X-12, P_Y-24))
        
        # Update ship position and rotation
        mx, my = pygame.mouse.get_pos()
        ship_rect = ship.get_rect(topleft=(P_X, P_Y))
        dx, dy = mx - ship_rect.centerx, ship_rect.centery - my
        angle = math.degrees(math.atan2(-dx, dy))
        rot_image = pygame.transform.rotate(ship, angle)
        rot_image_rect = rot_image.get_rect(center=ship_rect.center)
        surface.blit(rot_image, rot_image_rect.topleft)
        
        # Check for asteroid collisions with ship
        for roid in asteroids[:]:
            if roid.rect.colliderect(ship_rect):
                health -= 1
                asteroids.remove(roid)
        
        # Update and draw lasers
        for laser in lasers[:]:
            laser.update()
            rad = math.radians(laser.angle)
            end_x = laser.x + math.cos(rad) * laser.length
            end_y = laser.y - math.sin(rad) * laser.length
            
            # Check for laser hits on asteroids
            for roid in asteroids[:]:
                if roid.rect.clipline((laser.x, laser.y), (end_x, end_y)):
                    if laser in lasers:
                        lasers.remove(laser)
                    if roid in asteroids:
                        asteroids.remove(roid)
                    hit_asteroids += 1
                    break
            
            # Remove lasers that are off screen
            if laser.x < 0 or laser.x > width or laser.y < 0 or laser.y > height:
                if laser in lasers:
                    lasers.remove(laser)
            else:
                laser.draw(surface)
        
        # Update and draw asteroids
        for roid in asteroids[:]:
            roid.update()
            if roid.x < -60 or roid.x > width + 60 or roid.y < -60 or roid.y > height + 60:
                asteroids.remove(roid)
            else:
                roid.draw(surface)
        
        # Spawn new asteroids
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            rand_choice = random.random()
            if rand_choice < 0.1:
                asteroids.append(Asteroid(1, speed, random.randint(90, 180)))
            elif rand_choice < 0.15:
                asteroids.append(Asteroid(2, speed, random.randint(90, 180)))
            elif rand_choice < 0.18:
                asteroids.append(Asteroid(3, speed, random.randint(90, 180)))
        
        # Update the display
        screen_display.update()
        clock.tick(60)
    
    pygame.quit()
    accuracy = hit_asteroids / laser_count if laser_count > 0 else 0
    
    print('########### STATS ###########')
    print('Score:', hit_asteroids)
    print(f'Accuracy: {accuracy:.2%}')
    update_scoreboard(hit_asteroids)