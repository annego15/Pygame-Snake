import random
import pygame
from pygame.constants import *

#   R    G    B
GRAY = (100, 100, 100)
DARKGRAY  = ( 40,  40,  40)
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

board_length = 640
board_height = 540

cell_size = 20

assert board_length % cell_size == 0, "Window width must be a multiple of cell size."
assert board_height % cell_size == 0, "Window height must be a multiple of cell size."

gitter_size_length = board_length // cell_size
gitter_size_height = board_height // cell_size



class Spiel:
    def __init__(self, board_length, board_height, gitter_breite, gitter_hoehe, cell_size):
        self.board_length = board_length
        self.board_height = board_height
        self.gitter_breite = gitter_breite
        self.gitter_hoehe = gitter_hoehe
        self.cell_size = cell_size

        self.felder = [[0 for j in range(gitter_breite)] for i in range(gitter_hoehe)]

        # Rand, spricht schwarze Felder setzen
        for i in range(gitter_breite):
            self.felder[0][i] = 1
            self.felder[-1][i] = 1
        for i in range(gitter_hoehe):
            self.felder[i][0] = 1
            self.felder[i][-1] = 1

        self.der_rote = [random.randint(2, gitter_hoehe-2),
                         random.randint(2, gitter_breite-2)]

        self.bewegung = [0,0]

    def update_koordinaten(self):
        neues_i = self.der_rote[0] + self.bewegung[0]

        if self.felder[neues_i][self.der_rote[1]] != 1:
            self.der_rote[0] = neues_i

        neues_j = self.der_rote[1] + self.bewegung[1]

        if self.felder[self.der_rote[0]][neues_j] != 1:
            self.der_rote[1] = neues_j

    def draw_game(self, screen):
        self.draw_board(screen)
        self.draw_der_rote(screen)

    def draw_board(self, screen):
        for x in range(0, self.board_length, self.cell_size): # draw vertical lines
             pygame.draw.line(screen, DARKGRAY, (x, 0), (x, self.board_height))
        for y in range(0, self.board_height, cell_size): # draw horizontal lines
             pygame.draw.line(screen, DARKGRAY, (0, y), (self.board_length, y))

        for i in range(len(self.felder)):
            for j in range(len(self.felder[i])):
                if self.felder[i][j] == 1:
                    x, y = self.board_to_pixel_koord(i,j)
                    a_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, BLACK, a_rect)

    def draw_der_rote(self, screen):
        x, y = self.board_to_pixel_koord(self.der_rote[0], self.der_rote[1])
        a_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        pygame.draw.rect(screen, RED, a_rect)

    def board_to_pixel_koord(self, i, j):
        return j * self.cell_size, i * self.cell_size

    def pixel_to_board_koord(self, x, y, width):
        return y // width, x // width


def main():
    pygame.init()
    my_game = Spiel(board_length, board_height, gitter_size_length,
                    gitter_size_height, cell_size)

    screen = pygame.display.set_mode((board_length, board_height), 0, 32)
    pygame.display.set_caption('Gitterbeispiel')

    FPS = 10  # frames per second setting
    fps_clock = pygame.time.Clock()
    is_running = True
    while is_running: # the main game loop
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                is_running = False

            elif event.type == pygame.KEYDOWN:
                # Der Rote
                if event.key == pygame.K_DOWN:
                     my_game.bewegung[0] = 1
                elif event.key == pygame.K_UP:
                    my_game.bewegung[0] = -1
                elif event.key == pygame.K_LEFT:
                    my_game.bewegung[1] = -1
                elif event.key == pygame.K_RIGHT:
                    my_game.bewegung[1] = 1
            elif event.type == pygame.KEYUP:
                # Der Rote
                if event.key == pygame.K_DOWN:
                     my_game.bewegung[0] = 0
                elif event.key == pygame.K_UP:
                    my_game.bewegung[0] = 0
                elif event.key == pygame.K_LEFT:
                    my_game.bewegung[1] = 0
                elif event.key == pygame.K_RIGHT:
                    my_game.bewegung[1] = 0

        my_game.update_koordinaten()
        my_game.draw_game(screen)

        pygame.display.update()
        fps_clock.tick(FPS)

if __name__ == '__main__':
    main()