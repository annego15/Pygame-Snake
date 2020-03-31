import pygame
from pygame.constants import *

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
BLUE      = (  0,   0, 255)
DARKGRAY  = ( 40,  40,  40)

pygame.init()

# Fenstergroesse
board_length = 900
board_height = 700

# Das Fenster erstellen
screen = pygame.display.set_mode((board_length, board_height), 0, 32)
pygame.display.set_caption('Ein Fenstertitel')

screen.fill(WHITE)
pygame.display.update()
is_running = True
while is_running: # main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

pygame.quit()
print("Programm beendet.")