from game import *
import math


class AiFollow(Player):
    def __init__(self, game, color):
        super().__init__(game, color, ai=True)
        self.game = game
        self.players = []

    def pass_players(self, players):
        self.players = players

    def update_ai(self):
        self.compute_direction()

    def compute_direction(self):
        # calculate vector with vector-geo (flipped y because y-axis is flipped)
        vector = (self.game.food_x - self.snake_tiles_x[0], self.snake_tiles_y[0] - self.game.food_y)
        # calculate angle to food with angle = tan^-1(y/x)
        angle = math.atan2(vector[1], vector[0])/math.pi
        print("Vector {} / {} angle: {}".format(vector[0], vector[1], angle))
        if 0.25 <= angle < 0.75:
            self.direction = self.find_good_dir(0)
        elif 0.75 <= angle or angle < -0.75:
            self.direction = self.find_good_dir(1)
        elif -0.75 <= angle < -0.25:
            self.direction = self.find_good_dir(2)
        else:
            self.direction = self.find_good_dir(3)

    def find_good_dir(self, new_dir):
        try_dir = new_dir
        for add_dir in (0, 1, 3, 2):
            try_dir = (new_dir + add_dir) % 4
            x, y = self.calc_new_head_pos(try_dir)

            found_collision = False
            for player in self.players:
                for i in range(len(player.snake_tiles_x)):
                    if x == player.snake_tiles_x[i] and \
                            y == player.snake_tiles_y[i]:
                        # found collision with other player
                        found_collision = True
                        break

            if not found_collision:
                # found direction which works
                break
        else:
            print("At this moment he realised: He is fucked!")
            return self.direction

        # return direction which works
        print("Ai dir to food: {}, dir to avoid collision: {}".format(new_dir, try_dir))
        return try_dir




