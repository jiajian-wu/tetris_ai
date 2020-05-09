# Import a library of functions called 'pygame'
import pygame
from math import pi

# Initialize the game engine
from pygame.rect import Rect

pygame.init()

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the height and width of the screen
size = [400, 400]
screen = pygame.display.set_mode(size)


# class to store all the sitting blocks
class Block_List:
    pos_s = set()  # set to store positions of the sitting blocks in "top:left" fashion.
    bl = []  # list to hold all the blocks

    def draw_all(self, surface):
        for block in self.bl:
            block.draw(surface)

    def append(self, b):
        self.bl.append(b)
        self.pos_s.add(b.block.topleft)


class Block(Rect):
    def __init__(self):
        self.block = Rect(20, 20, 20, 20)

    def collide_down(self, s):
        if self.block.bottomleft in s:
            return True
        return False

    # def collide_left(self, l):

    def key_press(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.block.move_ip(-20, 0)
        if key[pygame.K_RIGHT]:
            self.block.move_ip(20, 0)
        if key[pygame.K_UP]:
            self.block.move_ip(0, -20)
        if key[pygame.K_DOWN]:
            # to add instant drop function
            self.block.move_ip(0, 20)

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.block)


done = False
clock = pygame.time.Clock()

block_list = Block_List()
curr_block = Block()

while not done:

    clock.tick(10)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    screen.fill(WHITE)

    curr_block.key_press()
    print(block_list.pos_s, "bottom left pos ", curr_block.block.bottomleft)

    if curr_block.block.bottom > 300 or curr_block.collide_down(block_list.pos_s):
        block_list.append(curr_block)  # add to sitting blocks then create a new block
        print(len(block_list.bl))
        curr_block = Block()

    curr_block.draw(screen)  # draw the falling block

    block_list.draw_all(screen)  # draw all the siting blocks

    pygame.display.flip()

pygame.quit()
