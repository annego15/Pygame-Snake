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

board_length = 900
board_height = 700

class My_Circle:
    def __init__(self, x, y, movex, movey):
        self.koordinaten = {}
        self.koordinaten["x"] = x
        self.koordinaten["y"] = y
        self.move = {}
        self.move["x"] = movex
        self.move["y"] = movey

    def update(self):
        if self.koordinaten["x"] + self.move["x"] >= board_length or \
                    self.koordinaten["x"] + self.move["x"] <= 0:
            self.move["x"] *= -1
        self.koordinaten["x"] += self.move["x"]
        if self.koordinaten["y"] + self.move["y"] >= board_height or \
                    self.koordinaten["y"] + self.move["y"] <= 0:
            self.move["y"] *= -1
        self.koordinaten["y"] += self.move["y"]

def main():
    pygame.init()

    screen = pygame.display.set_mode((board_length, board_height), 0, 32)
    pygame.display.set_caption('Der bewegte Kreis')

    step_size = 5
    FPS = 60  # frames per second setting
    fps_clock = pygame.time.Clock()
    the_circ = My_Circle(300, 450, step_size, 2)
    is_running = True
    while is_running: # main game loop
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                is_running = False

        the_circ.update()

        pygame.draw.circle(screen, ORANGE, (the_circ.koordinaten["x"],
                                            the_circ.koordinaten["y"]), 10, 0)
        print_background(screen)

        pygame.display.update()
        fps_clock.tick(FPS)

    pygame.quit()

def print_background(screen):
    pygame.draw.rect(screen, RED, (500, 20, 100, 100), 1)
    pygame.draw.rect(screen, BLUE, (200, 500, 200, 100), 0)
    pygame.draw.polygon(screen, GREEN, ((146, 0), (291, 106), (236, 277),
                                        (56, 277), (0, 106)))

if __name__ == "__main__":
    main()
    print("Programm beendet.")