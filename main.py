# import pygame module 
import pygame 
import gamestate
import math

width = 800
height = 600
z = [width,height] 
transparent = (0, 0, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)

# Set screen 
screen_display = pygame.display 
screen_display.set_caption('Asteroids') 
surface = screen_display.set_mode(z) 
pygame.font.init()
font = pygame.font.Font('Platinum Sign.ttf', 32)
font2 = pygame.font.SysFont('Arial', 32)

######################## Choose Difficulty ########################

difficulty = int(input('Enter Difficulty:\n 1 Easy \n 2 Normal \n 3 Hard \n'))

############################# GAME START ####################################

pygame.init() 
# --- Title Screen Loop ---
title_screen = True
while title_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Press any key or mouse click to start the game
        if event.type == pygame.MOUSEBUTTONDOWN:
            title_screen = False
    surface.fill(white)
    text = font.render('ASTEROIDS', True, black)
    text2 = font2.render('click to play', True, black)
	
    textRect = text.get_rect()
    textRect2 = text2.get_rect()
    
    textRect.center = (width / 2, height / 2)
    textRect2.center = (width / 2, height / 2 + 50)
    
    surface.blit(text, textRect)
    surface.blit(text2, textRect2)
    pygame.display.update()


gamestate.playing(surface, difficulty)
pygame.quit() 

gamestate.print_board()
