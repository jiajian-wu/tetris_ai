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


class Block(Rect):
    def __init__(self):
        self.block = Rect(20, 20, 20, 20)

    def collide(self, l):
        pos_dict = {}
        for b in l:
            pos_dict[b.block.top] = b.block.left
            if self.block.bottom in pos_dict and self.block.left == pos_dict[self.block.bottom]:
                return True
        return False



    def key_press(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.block.move_ip(-20, 0)
        if key[pygame.K_RIGHT]:
            self.block.move_ip(20, 0)
        if key[pygame.K_UP]:
            self.block.move_ip(0, -20)
        if key[pygame.K_DOWN]:
            self.block.move_ip(0, 20)

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.block)


done = False
clock = pygame.time.Clock()

block_list = []
curr_block = Block()

while not done:

    clock.tick(10)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    screen.fill(WHITE)

    curr_block.key_press()

    print("sitting block top and left position", curr_block.block.topleft)

    if curr_block.block.bottom > 300 or curr_block.collide(block_list):
        block_list.append(curr_block)   # add to sitting blocks then create a new block
        curr_block = Block()

    curr_block.draw(screen)  # draw the falling block

    for b in block_list:
        b.draw(screen)  # draw all the siting blocks

    pygame.display.flip()

pygame.quit()
