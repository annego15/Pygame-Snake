import pygame
from pygame.constants import *

#            R    G    B
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
BLACK = (0,0,0)

class Tier(pygame.sprite.Sprite):
    def __init__(self, bild, x = 0, y = 0):
        super().__init__()
        self.image = pygame.image.load(bild) # Eigentlich ein Surface
        self.rect = self.image.get_rect()
        self.set_pos(x, y)

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def add_to_pos(self, x, y):
        self.rect.x += x
        self.rect.y += y

class Wall(pygame.sprite.Sprite):
    def __init__(self, color, x , y , width, height):
        super().__init__()
        self.image = pygame.Surface((width,height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def main():
    pygame.init()

    FPS = 30 # frames per second setting
    fpsClock = pygame.time.Clock()

    board_length = 700
    board_height = 500
    wand_delta = 10

    step_size = 5

    # set up the window
    screen = pygame.display.set_mode((board_length, board_height), 0, 32)
    pygame.display.set_caption('The Mouse')

    my_mouse = Tier('mouse2.png', 70, 70)
    movex, movey = 0, 0

    wall_1 = Wall(BLACK, 0,0, board_length, wand_delta)
    wall_2 = Wall(BLACK, 0,0, wand_delta, board_height)
    wall_3 = Wall(BLACK, 0,board_height-wand_delta, board_length, wand_delta)
    wall_4 = Wall(BLACK, board_length - wand_delta, 0, wand_delta, board_height)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(my_mouse, wall_1, wall_2, wall_3, wall_4)

    is_running = True

    while is_running: # the main game loop
        screen.fill(WHITE)

        my_mouse.add_to_pos(movex, movey)

        collide_w1 = pygame.sprite.collide_rect(my_mouse, wall_1)
        collide_w2 = pygame.sprite.collide_rect(my_mouse, wall_2)
        collide_w3 = pygame.sprite.collide_rect(my_mouse, wall_3)
        collide_w4 = pygame.sprite.collide_rect(my_mouse, wall_4)

        if collide_w1:
            my_mouse.add_to_pos(0,step_size)
        if collide_w2:
            my_mouse.add_to_pos(step_size, 0)
        if collide_w3:
            my_mouse.add_to_pos(0, -step_size)
        if collide_w4:
            my_mouse.add_to_pos(-step_size, 0)

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                is_running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    is_running = False
                elif event.key == K_a:
                    movex = -step_size
                elif event.key == K_d:
                    movex = step_size
                elif event.key == K_w:
                    movey = -step_size
                elif event.key == K_s:
                    movey = step_size

            elif event.type == KEYUP:
                if event.key == K_a or event.key == K_d:
                    movex = 0
                if event.key == K_w or event.key == K_s:
                    movey = 0

        all_sprites.draw(screen)
        pygame.display.update()
        fpsClock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
    print("Ferig")