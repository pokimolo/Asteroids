import pygame
import math

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

# Background
bg = pygame.image.load('pictures/Bg.jpg')
bg = pygame.transform.scale(bg, (width, height))


class Laser:
    def __init__(self, angle):
        self.x = width / 2
        self.y = height / 2
        self.angle = angle + 90  # offset to match the angle of the ship
        self.speed = 3  # speed of the laser
        self.length = 10  # length of the laser

        # Calculate the velocity based on the angle
        rad = math.radians(self.angle)
        self.dx = math.cos(rad) * self.speed
        self.dy = -math.sin(rad) * self.speed  # Flip the y-direction

    def update(self):
        # Update position of the laser
        self.x += self.dx
        self.y += self.dy

    def draw(self, surface):
        # Draw the laser line with its current position
        rad = math.radians(self.angle)
        end_x = self.x + math.cos(rad) * self.length
        end_y = self.y - math.sin(rad) * self.length  # Fix: Offset the laser drawing

        pygame.draw.line(surface, red, (self.x, self.y), (end_x, end_y), 4)


def playing(surface):
    pygame.init()
    window = True
    lasers = []  # List to store lasers
    laser_count = 0 # use for accuracy displayed later

    while window:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window = False
            # Shoot laser on mouse button down
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Create laser at the ship's center, with the current angle
                lasers.append(Laser(angle))
                laser_count +=1
        #make background
        surface.blit(bg, (0, 0))

        # Using mouse position to angle ship
        mx, my = pygame.mouse.get_pos()
        ship_rect = ship.get_rect(topleft=(P_X, P_Y))
        dx, dy = mx - ship_rect.centerx, ship_rect.centery - my
        angle = math.degrees(math.atan2(-dx, dy))

        # Rotate the ship image to the new angle
        rot_image = pygame.transform.rotate(ship, angle)
        rot_image_rect = rot_image.get_rect(center=ship_rect.center)
        surface.blit(rot_image, rot_image_rect.topleft)

        # Update and draw each laser
        for laser in lasers[:]:
            laser.update()
            if laser.x < 0 or laser.x > width or laser.y < 0 or laser.y > height:
                lasers.remove(laser)  # Remove laser if off-screen
            else:
                laser.draw(surface)  # Draw the laser

        screen_display.update()

    pygame.quit()