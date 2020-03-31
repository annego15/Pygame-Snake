import pygame, sys
from pygame.locals import *

# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

def main():

    pygame.init()

    # set up the window
    D_WIDHT = 600
    D_HEIGHT = 300

    DISPLAYSURF = pygame.display.set_mode((D_WIDHT, D_HEIGHT), 0, 32)
    pygame.display.set_caption('Drawing')


    die_koordinaten = {'x': 300, 'y': 200}

    delta_x = 2

    FPS = 50
    FPSCLOCK = pygame.time.Clock()

    while True:
        DISPLAYSURF.fill(WHITE)
        for event in pygame.event.get():

            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        the_background(DISPLAYSURF)

        die_koordinaten['x'] = (die_koordinaten['x'] + delta_x) % D_WIDHT
        pygame.draw.circle(DISPLAYSURF, BLACK, (die_koordinaten['x'], die_koordinaten['y']), 5, 0)


        pygame.display.update()
        FPSCLOCK.tick(FPS)


def the_background(surface):
    # draw on the surface object
    surface.fill(WHITE)
    pygame.draw.polygon(surface, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))
    pygame.draw.line(surface, BLUE, (60, 60), (120, 60), 4)
    pygame.draw.line(surface, BLUE, (120, 60), (60, 120))
    pygame.draw.line(surface, BLUE, (60, 120), (120, 120), 4)
    pygame.draw.circle(surface, BLUE, (300, 50), 20, 0)
    pygame.draw.ellipse(surface, RED, (300, 200, 40, 80), 1)
    the_rect = pygame.Rect(300, 200, 40, 80)
    pygame.draw.rect(surface, BLACK, the_rect, 1)
    pygame.draw.rect(surface, RED, (200, 150, 100, 50))

# run the game loop
if __name__ == "__main__":
    main()