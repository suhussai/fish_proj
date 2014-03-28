import pygame
import sys
import pyganim
from pygame.locals import *
import time
from fish_artist import FishArtist
from random import randint
from random import random
#http://stackoverflow.com/questions/5555712/generate-a-random-number-in-python
#from handler import DrawHandling

pygame.init()


SCREEN_HEIGHT = 300 + 400
SCREEN_WIDTH = 470 + 400
background = pygame.image.load('fishdish/fishtitle.png')
#background.blit()
#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.set_mode((background.get_width(), background.get_height()))
print(screen.get_rect())
#bg_layer = 

clock = pygame.time.Clock()

#http://stackoverflow.com/questions/9961563/how-can-i-make-a-sprite-move-when-key-is-held-down
BGCOLOR = (10, 10, 100)
#Red, Green, Blue
main_fish = FishArtist(screen, 300, 200, '7main_fish', 1)

#yellow fish needs fixing
#grey fish needs fixing
#purple fish too
#green fish too
#small yellow fish too

#1main too , 2, 5, 6, 7
#3 good , 4
start_screen = True
game = False

while 1:
    if start_screen:
        screen.blit(background,(0,0))

    if game:
        main_fish.stationary_fish_movements(10)
        main_fish.keys_pressed_response(pygame.key.get_pressed())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()

        if (event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE)):
            pygame.display.quit()
            sys.exit()

#            main_fish.grow()

        if (event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN) and start_screen):
            game = True
            start_screen = False
            screen.fill(BGCOLOR)
            
            

        if ((event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT) and game):
            main_fish.move_right()

        if ((event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT) and game):
            main_fish.move_left()

        if ((event.type == pygame.KEYDOWN and event.key == pygame.K_UP) and game):
            main_fish.move_up()

        if ((event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN) and game):
            main_fish.move_down()

        main_fish.get_pos()

        main_fish.fish_collision(None)
    pygame.display.update()
    clock.tick(30) # clock to slow down (only being called 30 times per second)



