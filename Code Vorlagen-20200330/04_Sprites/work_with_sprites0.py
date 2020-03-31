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

class Wall(pygame.sprite.Sprite): # Eigentlich Rechtecke
    def __init__(self, color, x , y , width, height):
        super().__init__()
        self.image = pygame.Surface((width,height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

def main():
    pygame.init()

    FPS = 30 # frames per second setting
    fpsClock = pygame.time.Clock()

    board_length = 700
    board_height = 600

    # set up the window
    screen = pygame.display.set_mode((board_length, board_height), 0, 32)
    pygame.display.set_caption('The Wall')


    mouse_pos = [100, 0]
    wall_1 = Wall(BLACK, 100,0, 10, 150)
    wall_2 = Wall(BLACK, 300, 200, 50, 10)
    
    wall_sprites = pygame.sprite.Group()
    wall_sprites.add(wall_1, wall_2)

    is_running = True
    is_mouse_Clicked = False
    while is_running: # the main game loop
        screen.fill(WHITE)

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                is_running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    is_running = False

            elif event.type == MOUSEBUTTONUP:
                mouse_pos = event.pos
                is_mouse_Clicked = True

        if is_mouse_Clicked:
            wall_1.set_pos(mouse_pos[0], mouse_pos[1])
            is_mouse_Clicked = False

        wall_sprites.draw(screen)
        pygame.display.update()
        fpsClock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
    print("Ferig")