import pygame
import random

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)


class Game:
    def __init__(self, screen, board_length, board_height, cell_size):
        self.board_length = board_length
        self.board_height = board_height
        self.cell_size = cell_size

        self.coordinates_length = self.board_length // self.cell_size
        self.coordinates_height = self.board_height // self.cell_size
        self.food_x = random.randint(0, self.coordinates_length - 1)
        self.food_y = random.randint(0, self.coordinates_height - 1)
        self.screen = screen
        self.game_over = False
        self.players = []
        x, y = self.to_pixel(self.food_x, self.food_y)
        self.food_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)

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
                        player.game_over_player = True
                        break

        # remove players which are game over
        for player in self.players:
            if player.game_over_player:
                self.players.remove(player)
                del player

        # update food position if eaten
        if food_eaten:
            found_good_position = False
            while not found_good_position:
                self.food_x = random.randint(0, self.coordinates_length - 1)
                self.food_y = random.randint(0, self.coordinates_height - 1)
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
            self.food_rect.x, self.food_rect.y = self.to_pixel(self.food_x, self.food_y)

    def draw_game(self):
        self.screen.fill(BLACK)
        # draw all players
        for player in self.players:
            player.draw_player(self.screen)
        # draw food
        pygame.draw.rect(self.screen, RED, self.food_rect)

    def to_pixel(self, x, y):
        return x * self.cell_size, y * self.cell_size


class Player:
    def __init__(self, game, color, key_up=None, key_left=None, key_down=None, key_right=None, ai=False):
        self.game = game
        self.color = color
        self.key_up = key_up
        self.key_left = key_left
        self.key_down = key_down
        self.key_right = key_right

        self.ai = ai

        self.snake_tiles_x = [random.randint(self.game.coordinates_length // 4,
                              (self.game.coordinates_length // 4) * 3)]
        self.snake_tiles_y = [random.randint(self.game.coordinates_length // 4,
                              (self.game.coordinates_length // 4) * 3)]
        self.direction = 0      # 0 = up, 1 = left, 2 = down, 3 = right
        self.last_direction = 0
        self.game_over_player = False
        self.food_eaten = False
        self.player_rect = pygame.Rect(0, 0, self.game.cell_size, self.game.cell_size)
        self.game.add_player(self)

    def calc_new_head_pos(self, direction):
        if direction == 0:
            return self.snake_tiles_x[0], self.snake_tiles_y[0] - 1
        elif direction == 1:
            return self.snake_tiles_x[0] - 1, self.snake_tiles_y[0]
        elif direction == 2:
            return self.snake_tiles_x[0], self.snake_tiles_y[0] + 1
        elif direction == 3:
            return self.snake_tiles_x[0] + 1, self.snake_tiles_y[0]

    def update_player(self, game):
        x, y = self.calc_new_head_pos(self.direction)
        self.last_direction = self.direction

        if x >= self.game.coordinates_length or y >= self.game.coordinates_height or x < 0 or y < 0:
            self.game_over_player = True

        for i in range(len(self.snake_tiles_x)):
            if self.snake_tiles_x[i] == x and self.snake_tiles_y[i] == y:
                self.game_over_player = True

        self.snake_tiles_x.insert(0, x)
        self.snake_tiles_y.insert(0, y)

        if not self.food_eaten:
            self.snake_tiles_x.pop(-1)
            self.snake_tiles_y.pop(-1)

        self.food_eaten = False
        for i in range(len(self.snake_tiles_x)):
            if self.snake_tiles_x[i] == game.food_x and self.snake_tiles_y[i] == game.food_y:
                self.food_eaten = True

    def draw_player(self, screen):
        for i in range(len(self.snake_tiles_x)):
            self.player_rect.x, self.player_rect.y = self.game.to_pixel(self.snake_tiles_x[i], self.snake_tiles_y[i])
            pygame.draw.rect(screen, self.color, self.player_rect)

    def change_direction(self, event):
        if event.key == self.key_up:
            new_dir = 0
        elif event.key == self.key_left:
            new_dir = 1
        elif event.key == self.key_down:
            new_dir = 2
        elif event.key == self.key_right:
            new_dir = 3
        else:
            return

        if len(self.snake_tiles_x) == 1:
            self.direction = new_dir
        else:
            # don't run into yourself
            if self.last_direction != (new_dir+2) % 4:
                self.direction = new_dir

    def change_direction_ai(self, direction):
        if 0 <= direction <= 3:
            self.direction = direction
