import pygame
import random
from pygame.locals import *

board_length = 640
board_height = 540

cell_size = 20

assert board_length % cell_size == 0, "Window width must be a multiple of cell size."
assert board_height % cell_size == 0, "Window height must be a multiple of cell size."

coordinates_length = board_length // cell_size
coordinates_height = board_height // cell_size

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)


class Player:
    def __init__(self, game, color_, key_up_, key_right_, key_down_, key_left_):
        self.color = color_
        self.key_up = key_up_
        self.key_right = key_right_
        self.key_down = key_down_
        self.key_left = key_left_
        self.snake_tiles_x = [random.randint(coordinates_length // 4, (coordinates_length // 4) * 3)]
        self.snake_tiles_y = [random.randint(coordinates_length // 4, (coordinates_length // 4) * 3)]
        self.direction = 0      # 0 = up, 1 = right, 2 = down, 3 = left
        self.game_over_player = False
        self.food_eaten = False
        self.player_rect = pygame.Rect(0, 0, cell_size, cell_size)
        game.add_player(self)

    def update_player(self, game):
        if self.direction == 0:
            self.check_cell(self.snake_tiles_x[0], self.snake_tiles_y[0] - 1)
        elif self.direction == 1:
            self.check_cell(self.snake_tiles_x[0] + 1, self.snake_tiles_y[0])
        elif self.direction == 2:
            self.check_cell(self.snake_tiles_x[0], self.snake_tiles_y[0] + 1)
        elif self.direction == 3:
            self.check_cell(self.snake_tiles_x[0] - 1, self.snake_tiles_y[0])

        if not self.food_eaten:
            self.snake_tiles_x.pop(-1)
            self.snake_tiles_y.pop(-1)

        self.food_eaten = False
        for i in range(len(self.snake_tiles_x)):
            if self.snake_tiles_x[i] == game.food_x and self.snake_tiles_y[i] == game.food_y:
                self.food_eaten = True

    def check_cell(self, x, y):
        if x >= coordinates_length or y >= coordinates_height or x < 0 or y < 0:
            self.game_over_player = True

        for i in range(len(self.snake_tiles_x)):
            if self.snake_tiles_x[i] == x and self.snake_tiles_y[i] == y:
                self.game_over_player = True

        self.snake_tiles_x.insert(0, x)
        self.snake_tiles_y.insert(0, y)

    def draw_player(self, screen):
        for i in range(len(self.snake_tiles_x)):
            self.player_rect.x, self.player_rect.y = to_pixel(self.snake_tiles_x[i], self.snake_tiles_y[i])
            pygame.draw.rect(screen, self.color, self.player_rect)


def to_pixel(x, y):
    return x * cell_size, y * cell_size


class Game:
    def __init__(self, screen_):
        self.food_x = random.randint(0, coordinates_length - 1)
        self.food_y = random.randint(0, coordinates_height - 1)
        self.screen = screen_
        self.game_over = False
        self.players = []
        x, y = to_pixel(self.food_x, self.food_y)
        self.food_rect = pygame.Rect(x, y, cell_size, cell_size)

    def add_player(self, player):
        self.players.append(player)

    def update_game(self):
        food_eaten = False

        # update every player movement
        for player in self.players:
            player.update_player(self)
            if player.food_eaten:
                food_eaten = True

        # check for collisions with other players
        for player in self.players:
            other_players = self.players[:]
            other_players.remove(player)
            for other_player in other_players:
                for i in range(len(other_player.snake_tiles_x)):
                    if player.snake_tiles_x[0] == other_player.snake_tiles_x[i] and \
                       player.snake_tiles_y[0] == other_player.snake_tiles_y[i]:
                        player.game_over = True

        # remove players which are game over
        for player in self.players:
            if player.game_over_player:
                self.players.remove(player)
                del player

        # update food position if eaten
        if food_eaten:
            found_good_position = False
            while not found_good_position:
                self.food_x = random.randint(0, coordinates_length - 1)
                self.food_y = random.randint(0, coordinates_height - 1)
                found_good_position = True

                for player in self.players:
                    for i in range(len(player.snake_tiles_x)):
                        # no collision recognized yet
                        if found_good_position:
                            if player.snake_tiles_x[i] == self.food_x and player.snake_tiles_y[i] == self.food_y:
                                # food collision with snake found
                                found_good_position = False
                                break
                # repeat loop if collision is found
            # update position of food if good new position is found
            self.food_rect.x, self.food_rect.y = to_pixel(self.food_x, self.food_y)

    def draw_game(self):
        self.screen.fill(BLACK)
        # draw all players
        for player in self.players:
            player.draw_player(self.screen)
        # draw food
        pygame.draw.rect(self.screen, RED, self.food_rect)


def change_direction(player, event):
    if event.key == player.key_up:
        new_dir = 0
    elif event.key == player.key_right:
        new_dir = 1
    elif event.key == player.key_down:
        new_dir = 2
    elif event.key == player.key_left:
        new_dir = 3
    else:
        return

    if len(player.snake_tiles_x) == 1:
        player.direction = new_dir
    else:
        if player.direction != (new_dir+2) % 4:
            player.direction = new_dir


def main():
    pygame.init()

    screen = pygame.display.set_mode((board_length, board_height), 0, 32)
    pygame.display.set_caption('Snake')

    my_game = Game(screen)
    Player(my_game, GREEN, K_w, K_d, K_s, K_a)
    Player(my_game, BLUE, K_UP, K_RIGHT, K_DOWN, K_LEFT)
    Player(my_game, CYAN, K_u, K_k, K_j, K_h)

    fps = 10  # frames per second setting
    fps_clock = pygame.time.Clock()
    is_running = True
    while is_running:   # the main game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                is_running = False
            elif event.type == KEYDOWN:
                # change direction if keys pressed
                for player in my_game.players:
                    change_direction(player, event)

        my_game.update_game()

        if not my_game.players:
            is_running = False
        else:
            my_game.draw_game()

            pygame.display.update()
            fps_clock.tick(fps)


if __name__ == '__main__':
    main()
