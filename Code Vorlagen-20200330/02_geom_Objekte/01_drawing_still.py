import pygame
from pygame.constants import *

#   R    G    B
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
pygame.init()

# Fenstergroesse
board_length = 900
board_height = 700

# Das Fenster erstellen
screen = pygame.display.set_mode((board_length, board_height), 0, 32)
pygame.display.set_caption('Ein Fenstertitel')

is_running = True
while is_running: # main game loop
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
                (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            is_running = False

    pygame.draw.rect(screen, RED, (500,20,100,100), 1)
    pygame.draw.rect(screen, BLUE, (200, 500, 200, 100), 0)
    pygame.draw.polygon(screen, GREEN, ((146, 0), (291, 106), (236, 277),
                                        (56, 277), (0, 106)),0)
    pygame.draw.circle(screen, ORANGE, (300,450), 10, 0)
    pygame.display.update()

pygame.quit()
print("Programm beendet.")