import pygame
from pygame.locals import *

from game import *
from ai import *

board_width = 640  # board width in pixels
board_height = 540  # board height in pixels

cell_size = 20  # pixels of a single coordinate

fps = 5  # frames per second setting

assert board_width % cell_size == 0, "Window width must be a multiple of cell size."
assert board_height % cell_size == 0, "Window height must be a multiple of cell size."


def main():
    pygame.init()

    screen = pygame.display.set_mode((board_width, board_height), 0, 32)
    pygame.display.set_caption('Snake')

    my_game = Game(screen, board_width, board_height, cell_size)
    ai1 = AiFollow(my_game, BLUE)
    Player(my_game, GREEN, K_w, K_a, K_s, K_d)
    #Player(my_game, BLUE, K_UP, K_LEFT, K_DOWN, K_RIGHT)
    #Player(my_game, CYAN, K_u, K_h, K_j, K_k)

    ai1.pass_players(my_game.players)

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
                    if not player.ai:
                        player.change_direction(event)

        ai1.update_ai()
        my_game.update_game()

        if not my_game.players:
            is_running = False
        else:
            my_game.draw_game()

            pygame.display.update()
            fps_clock.tick(fps)


if __name__ == '__main__':
    main()
