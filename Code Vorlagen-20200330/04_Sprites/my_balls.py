import pygame
from pygame.constants import *


#   R    G    B
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
BLACK = (0, 0, 0)

class __Abstract_Sprite:
    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def add_to_pos(self, x, y):
        self.rect.x += x
        self.rect.y += y


class Ball(pygame.sprite.Sprite, __Abstract_Sprite):
    """This class represents the ball."""
    def __init__(self, color = BLACK, radius = 5, x = 0, y = 0):
        super().__init__()
        self.image = pygame.Surface([2*radius, 2*radius], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, color, [radius, radius], radius, 0)
        self.rect = self.image.get_rect()
        self.set_pos(x, y)
        self.radius = radius

class Player(Ball):
    def __init__(self, color = BLACK, radius = 5, x = 0, y = 0):
        self.step_size = 1
        Ball.__init__(self, color, radius, x, y)

        self.movex = 0
        self.movey = 0

    def update_koordinaten(self, collide_list):
        self.add_to_pos(self.movex, 0)

        coll_object = pygame.sprite.spritecollideany(self, collide_list, False)
        if coll_object != None:
            if self.movex < 0:
                self.rect.left = coll_object.rect.right
            elif self.movex > 0:
                self.rect.right = coll_object.rect.left

        self.add_to_pos(0, self.movey)

        coll_object = pygame.sprite.spritecollideany(self, collide_list, False)
        if coll_object != None:
            if self.movey < 0:
                self.rect.top = coll_object.rect.bottom
            elif self.movey > 0:
                self.rect.bottom = coll_object.rect.top

    def handle_key_event(self, event=None):
        if not (event == None):
            if event.type == KEYDOWN:
                if event.key == K_a:
                    self.movex += -self.step_size
                if event.key == K_d:
                    self.movex += self.step_size
                if event.key == K_w:
                    self.movey += -self.step_size
                if event.key == K_s:
                    self.movey += self.step_size

            elif event.type == KEYUP:
                if event.key == K_a:
                    self.movex += self.step_size
                if event.key == K_d:
                    self.movex += -self.step_size
                if event.key == K_w:
                    self.movey += self.step_size
                if event.key == K_s:
                    self.movey += -self.step_size


class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Text_Block(pygame.sprite.Sprite):
    def __init__(self, text, fontObj, text_color=BLACK, background_color=WHITE, x=0, y=0):
        super().__init__()

        self.image = fontObj.render(text, True, text_color, background_color)
        self.rect = self.image.get_rect()
        self.set_pos(x, y)

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y




class Wall(pygame.sprite.Sprite):
    def __init__(self, color, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def main():
    pygame.init()

    FPS = 100  # frames per second setting
    fpsClock = pygame.time.Clock()

    board_length = 900
    board_height = 700

    # set up the window
    screen = pygame.display.set_mode((board_length, board_height), 0, 32)
    pygame.display.set_caption('The Shooter')

    wand_delta = 10
    wall_1 = Wall(BLACK, 0, 0, board_length, wand_delta)
    wall_2 = Wall(BLACK, 0, 0, wand_delta, board_height)
    wall_3 = Wall(BLACK, 0, board_height - wand_delta, board_length, wand_delta)
    wall_4 = Wall(BLACK, board_length - wand_delta, 0, wand_delta, board_height)

    wall_sprites = pygame.sprite.Group()
    wall_sprites.add(wall_1, wall_2, wall_3, wall_4)

    my_ball = Ball(BLUE, 20, 300, 300)
    my_ball2 = Ball(YELLOW, 20, 500, 300)
    my_ball3 = Ball(BLACK, 20, 600, 400)
    my_ball4 = Ball(NAVYBLUE, 20, 500, 50)

    balls_group = pygame.sprite.Group()
    balls_group.add(my_ball, my_ball2, my_ball3, my_ball4)

    my_player = Player(RED, 20, 200, 200)
    player_group = pygame.sprite.Group()
    player_group.add(my_player)

    is_running = True

    while is_running:  # the main game loop
        screen.fill(WHITE)

        my_player.update_koordinaten(wall_sprites)

        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                is_running = False

            my_player.handle_key_event(event)

        pygame.sprite.spritecollide(my_player, balls_group, True, pygame.sprite.collide_circle)

        wall_sprites.draw(screen)
        balls_group.draw(screen)
        player_group.draw(screen)
        pygame.display.update()
        fpsClock.tick(FPS)

        if len(balls_group.sprites()) == 0:
            is_running = False

    pygame.quit()


if __name__ == '__main__':
    main()
    print("Ferig")