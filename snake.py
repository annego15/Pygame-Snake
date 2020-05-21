import pygame
from pygame.locals import *

from screens import *

fps = 30  # frames per second setting

assert board_width % cell_size == 0, "Window width must be a multiple of cell size."
assert board_height % cell_size == 0, "Window height must be a multiple of cell size."


def main():
    pygame.init()

    screen = pygame.display.set_mode((board_width, board_height), 0, 32)
    pygame.display.set_caption('Snake')

    stage = MainScreen(screen)

    fps_clock = pygame.time.Clock()
    is_running = True
    while is_running:   # the main game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == KEYDOWN:
                stage.keypress(event)

        stage.render()

        pygame.display.update()
        fps_clock.tick(fps)

        stage = stage.next_stage
        if stage == "quit":
            is_running = False


if __name__ == '__main__':
    main()
