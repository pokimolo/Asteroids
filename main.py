# import pygame module 
import pygame 
import math

pygame.init() 

# width 
width = 1200

# height 
height = 800

#store he screen size 
z = [width,height] 

# store the color 
white = (255, 255, 255) 
screen_display = pygame.display 

# Set caption of screen 
screen_display.set_caption('Asteroids') 

# setting the size of the window 
surface = screen_display.set_mode(z) 

# set the image which to be displayed on screen 
ship = pygame.image.load('pictures\spaceship.png').convert()
P_X = width/2
P_Y = height/2
# set window true 
window = True
while window: 
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: 
			window = False
			
			# display white on screen other than image 
	surface.fill(white) 

	mx, my = pygame.mouse.get_pos()
	ship_rect = ship.get_rect(topleft=(P_X, P_Y))
	dx, dy = mx - ship_rect.centerx, ship_rect.centery - my
	angle = math.degrees(math.atan2(-dy, dx)) +180
	
	rot_image = pygame.transform.rotate(ship, angle)
	rot_image_rect = rot_image.get_rect(center=ship_rect.center)
	surface.blit(rot_image, rot_image_rect.topleft)



	screen_display.update() 

pygame.quit() 
