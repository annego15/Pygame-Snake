from pygame.locals import *
import pygame

from game import *
from ai import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 128)
DARK_RED = (128, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)

board_width = 640  # board width in pixels
board_height = 540  # board height in pixels

cell_size = 20  # pixels of a single coordinate

class MainScreen:
    def __init__(self, screen):
        self.screen = screen
        self.next_stage = self

        self.page = 0

        self.selection = 0
        self.buttons_img = pygame.image.load('buttons.png')
        self.tutorial_img = pygame.image.load('tutorial.png')
        self.credits_img = pygame.image.load('credits.png')
        self.selection_rect = pygame.Rect(50, 140, 260, 60)
        self.side_game = Game(screen, 260, 360, 20, 330, 140, DARK_RED)
        self.ai_side = AiFollow(self.side_game, DARK_BLUE)
        self.ai_side.pass_players(self.side_game.players)

        self.frame_counter = 1

        self.char_rect = pygame.Rect(0, 0, 18, 18)
        self.pixels_s = ((2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (2, 4), (1, 4), (0, 4))
        self.pixels_n = ((0, 4), (0, 3), (0, 2), (0, 1), (0, 0), (1, 1), (1, 2), (2, 2), (2, 3), (3, 3), (3, 4), (3, 2), (3, 1), (3, 0))
        self.pixels_a = ((0, 4), (0, 3), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (2, 2), (1, 2))
        self.pixels_k = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (1, 1), (2, 1), (2, 0), (3, 0))
        self.pixels_e = ((3, 4), (2, 4), (1, 4), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (3, 0), (1, 2), (2, 2), (3, 2))
        self.chars = (self.pixels_s, self.pixels_n, self.pixels_a, self.pixels_k, self.pixels_e)
        self.x_cords = (51, 151, 271, 391, 511)

    def keypress(self, event):
        if self.page == 0:
            if event.key == K_UP:
                self.selection -= 1
            elif event.key == K_DOWN:
                self.selection += 1
            elif event.key == K_RETURN:
                if self.selection == 0:
                    self.next_stage = StageGame(self.screen)
                elif self.selection == 1:
                    self.page = 1
                elif self.selection == 2:
                    self.page = 2
                elif self.selection == 3:
                    self.next_stage = "quit"
                # switch to screen according to selection
                pass
        elif self.page == 1:
            if event.key == K_ESCAPE:
                self.page = 0
        elif self.page == 2:
            if event.key == K_ESCAPE:
                self.page = 0

        if self.selection > 3:
            self.selection = 3
        elif self.selection < 0:
            self.selection = 0

    def render(self):

        self.screen.fill(BLACK)

        if self.page == 0:
            self.ai_side.update_ai()
            self.side_game.update_game()

            if self.ai_side.game_over_player:
                self.side_game.players.remove(self.ai_side)
                del self.ai_side
                self.ai_side = AiFollow(self.side_game, DARK_BLUE)
                self.ai_side.pass_players(self.side_game.players)

            if self.frame_counter > 90:
                self.side_game.draw_game()

                self.screen.blit(self.buttons_img, (50, 140))
                self.selection_rect.y = 140 + self.selection * 100
                pygame.draw.rect(self.screen, WHITE, self.selection_rect, width=5, border_radius=0)

            if self.frame_counter <= 50:
                y_cords = 221
            elif self.frame_counter >= 90:
                y_cords = 21
            else:
                y_cords = 200 - (self.frame_counter - 50)*5 + 21

            for i, char in enumerate(self.chars):
                for j, cords in enumerate(char):
                    if j < self.frame_counter / 3:
                        x, y = cords
                        self.char_rect.x = self.x_cords[i] + (x * 20)
                        self.char_rect.y = y_cords + (y * 20)
                        pygame.draw.rect(self.screen, GREEN, self.char_rect)

        elif self.page == 1:
            self.screen.blit(self.tutorial_img, (0, 0))
        elif self.page == 2:
            self.screen.blit(self.credits_img, (0, 0))

        self.frame_counter += 1


class StageGame:
    def __init__(self, screen):
        self.screen = screen
        self.next_stage = self

        self.my_game = Game(screen, board_width, board_height, cell_size)
        self.ai1 = AiFollow(self.my_game, BLUE)
        self.player = Player(self.my_game, GREEN, (K_w, K_UP), (K_a, K_LEFT), (K_s, K_DOWN), (K_d, K_RIGHT))
        self.ai1.pass_players(self.my_game.players)
        self.frame_counter = 0
        self.frame_ai_dead = 9999999999999
        self.game_over = False
        self.highscore = "ERROR"
        self.score = 0

        self.rect_cover = pygame.Surface((board_width, board_height), pygame.SRCALPHA, 32)
        self.rect_cover.fill((0, 0, 0, 127))
        self.game_over_img = pygame.image.load('game_over.png')

        self.font = pygame.font.Font('PixelGameFont.ttf', 32)


    def keypress(self, event):
        if not self.game_over:
            for player in self.my_game.players:
                if not player.ai:
                    player.change_direction(event)
        else:
            if event.key == K_RETURN:
                self.next_stage = MainScreen(self.screen)
                self.next_stage.frame_counter = 90

    def render(self):
        if not self.game_over:
            if (self.frame_counter % 6) == 0:
                self.ai1.update_ai()
                self.my_game.update_game()

                if self.ai1.game_over_player:
                    self.frame_ai_dead = self.frame_counter + 90
                    del self.ai1

                if self.player.game_over_player:
                    self.game_over = True
                    self.score = len(self.player.snake_tiles_x)

                    file = open("highscore_ai.txt", "r")
                    try:
                        stored_score = int(file.readline())
                        if stored_score < self.score:
                            file.close()
                            file = open("highscore_ai.txt", "w")
                            file.write(str(self.score))
                            self.highscore = self.score
                        else:
                            self.highscore = stored_score
                    except ValueError:
                        print("Error while reading file")
                    finally:
                        file.close()

                if self.frame_ai_dead < self.frame_counter:
                    self.frame_ai_dead = 999999999999
                    self.ai1 = AiFollow(self.my_game, BLUE)
                    self.ai1.pass_players(self.my_game.players)
            self.my_game.draw_game()
        else:
            self.my_game.draw_game()
            self.screen.blit(self.rect_cover, (0, 0))
            self.screen.blit(self.game_over_img, (30, 120))

            self.txt_to_screen('SCORE: ' + str(self.score), 300)
            self.txt_to_screen('HIGHSCORE: ' + str(self.highscore), 360)
            self.txt_to_screen('PRESS ENTER', 490)

        self.frame_counter += 1

    def txt_to_screen(self, txt_str, y):
        txt = self.font.render(txt_str, True, WHITE, BLACK)
        text_rect = txt.get_rect()
        text_rect.center = board_width // 2, y
        self.screen.blit(txt, text_rect)

