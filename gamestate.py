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

def playing(surface):
    pygame.init()
    window = True
    lasers = []
    asteroids = []
    laser_count = 0
    hit_asteroids = 0
    clock = pygame.time.Clock()
    health = 3
    spawn_timer = 0  # Timer to control spawn frequency
    spawn_interval = 20  # Set to the number of frames you want between spawns (60 frames = 1 second)

    while window and health > 0:
        # Draw background
        surface.blit(bg, (0, 0))

        # Check if quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                lasers.append(Laser(angle))
                laser_count += 1

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

        # Spin spaceship facing mouse x and y
        mx, my = pygame.mouse.get_pos()
        ship_rect = ship.get_rect(topleft=(P_X, P_Y))
        dx, dy = mx - ship_rect.centerx, ship_rect.centery - my
        angle = math.degrees(math.atan2(-dx, dy))
        rot_image = pygame.transform.rotate(ship, angle)
        rot_image_rect = rot_image.get_rect(center=ship_rect.center)
        surface.blit(rot_image, rot_image_rect.topleft)

        # Update lasers and check collisions
        for laser in lasers[:]:
            laser.update()
            rad = math.radians(laser.angle)
            end_x = laser.x + math.cos(rad) * laser.length
            end_y = laser.y - math.sin(rad) * laser.length

            for roid in asteroids[:]:
                if roid.rect.colliderect(ship_rect):
                    health -= 1
                    asteroids.remove(roid)
                    continue
                if roid.rect.clipline((laser.x, laser.y), (end_x, end_y)):
                    if laser in lasers:
                        lasers.remove(laser)
                    if roid in asteroids:
                        asteroids.remove(roid)
                        hit_asteroids += 1
                    break

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

        # Update spawn timer
        spawn_timer += 1  # Increment spawn timer by 1 frame each loop
        
        # Only spawn an asteroid if the timer has reached the spawn interval
        if spawn_timer >= spawn_interval:
            spawn_timer = 0  # Reset the spawn timer

            rand_choice = random.random()
            if rand_choice < 0.1:
                asteroids.append(Asteroid(1, .75, random.randint(90, 180)))  # Small asteroid
            elif rand_choice < 0.15:
                asteroids.append(Asteroid(2, .75, random.randint(90, 180)))  # Medium asteroid
            elif rand_choice < 0.18:
                asteroids.append(Asteroid(3, .75, random.randint(90, 180)))  # Large asteroid

        # Update the display
        screen_display.update()
        clock.tick(60)  # Limit the frame rate to 60 FPS

    pygame.quit()
    print('asteroids broken:', hit_asteroids)
    accuracy = hit_asteroids / laser_count if laser_count > 0 else 0
    print(f'accuracy: {accuracy:.2%}')
