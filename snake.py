import pygame
import random
from pygame.locals import *

board_length = 640
board_height = 540

cell_size = 20

assert board_length % cell_size == 0, "Window width must be a multiple of cell size."
assert board_height % cell_size == 0, "Window height must be a multiple of cell size."

gitter_size_length = board_length // cell_size
gitter_size_height = board_height // cell_size

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Game:
    def __init__(self, screen, cell_size):
        self.snake_tiles_x = [gitter_size_length//2]
        self.snake_tiles_y = [gitter_size_height//2]
        self.food_x = random.randint(0, gitter_size_length-1)
        self.food_y = random.randint(0, gitter_size_height - 1)
        self.food_eaten = False
        self.direction = 0      # 0 = up, 1 = right, 2 = down, 3 = left
        self.screen = screen
        self.cell_size = cell_size
        self.game_over = False

    def update_game(self):
        if self.direction == 0:
            self.check_cell(self.snake_tiles_x[0], self.snake_tiles_y[0] - 1)
        elif self.direction == 1:
            self.check_cell(self.snake_tiles_x[0] + 1, self.snake_tiles_y[0])
        elif self.direction == 2:
            self.check_cell(self.snake_tiles_x[0], self.snake_tiles_y[0] + 1)
        elif self.direction == 3:
            self.check_cell(self.snake_tiles_x[0] - 1, self.snake_tiles_y[0])

        if self.snake_tiles_x[0] >= gitter_size_length or self.snake_tiles_y[0] >= gitter_size_height \
                or self.snake_tiles_x[0] < 0 or self.snake_tiles_y[0] < 0:
            return False

        if not self.food_eaten:
            self.snake_tiles_x.pop(-1)
            self.snake_tiles_y.pop(-1)

        self.food_eaten = False
        found = False
        while not found:
            for i in range(len(self.snake_tiles_x)):
                if self.snake_tiles_x[i] == self.food_x and self.snake_tiles_y[i] == self.food_y:
                    self.food_eaten = True
                    self.food_x = random.randint(0, gitter_size_length - 1)
                    self.food_y = random.randint(0, gitter_size_height - 1)
                else:
                    found = True

    def check_cell(self, x, y):
        if x >= gitter_size_length or y >= gitter_size_height or x < 0 or y < 0:
            self.game_over = True

        for i in range(len(self.snake_tiles_x)):
            if self.snake_tiles_x[i] == x and self.snake_tiles_y[i] == y:
                self.game_over = True

        self.snake_tiles_x.insert(0, x)
        self.snake_tiles_y.insert(0, y)

    def draw_game(self):
        self.screen.fill(BLACK)
        for i in range(len(self.snake_tiles_x)):
            x, y = self.board_to_pixel_koord(self.snake_tiles_x[i], self.snake_tiles_y[i])
            a_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, GREEN, a_rect)
        x, y = self.board_to_pixel_koord(self.food_x, self.food_y)
        a_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, RED, a_rect)

    def board_to_pixel_koord(self, x, y):
        return x * self.cell_size, y * self.cell_size

def main():
    pygame.init()

    screen = pygame.display.set_mode((board_length, board_height), 0, 32)
    pygame.display.set_caption('Snake')

    my_game = Game(screen, cell_size)

    FPS = 5  # frames per second setting
    fps_clock = pygame.time.Clock()
    is_running = True
    while is_running: # the main game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                is_running = False
            elif event.type == KEYDOWN:
                #WASD
                if event.key == K_w:
                    my_game.direction = 0
                elif event.key == K_d:
                    my_game.direction = 1
                elif event.key == K_s:
                    my_game.direction = 2
                elif event.key == K_a:
                    my_game.direction = 3
                #
                elif event.key == K_UP:
                    my_game.direction = 0
                elif event.key == K_RIGHT:
                    my_game.direction = 1
                elif event.key == K_DOWN:
                    my_game.direction = 2
                elif event.key == K_LEFT:
                    my_game.direction = 3

        my_game.update_game()

        if my_game.game_over:
            is_running = False
        else:
            my_game.draw_game()

            pygame.display.update()
            fps_clock.tick(FPS)


if __name__ == '__main__':
    main()

