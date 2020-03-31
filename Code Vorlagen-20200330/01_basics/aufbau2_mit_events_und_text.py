import pygame, sys
from pygame.locals import *

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
BLUE      = (  0,   0, 255)
DARKGRAY  = ( 40,  40,  40)

board_length = 600
board_height = 200

pygame.init()

screen = pygame.display.set_mode((board_length, board_height), 0, 32)
pygame.display.set_caption('Ein Fenstertitel')

font_obj = pygame.font.Font('freesansbold.ttf', 32)
text_obj = font_obj.render('Start Text', True, BLACK)

rect_text = text_obj.get_rect() # Position des Textes setzen
rect_text.center = (board_length / 2, board_height / 2)

screen.fill(WHITE)
screen.blit(text_obj, rect_text)
is_running = True
while is_running: # main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
                (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            is_running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                screen.fill(WHITE)
                back_color =  BLACK
            elif event.button == 3:
                screen.fill(BLACK)
                back_color = WHITE

            text_obj = font_obj.render('Pressed ....', True, back_color)
            screen.blit(text_obj, rect_text)

    pygame.display.update()

pygame.quit()
print("Programm beendet.")