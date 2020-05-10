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
block_size = 50
row, col = 6, 6
color = RED
size = [block_size * col, block_size * row]
screen = pygame.display.set_mode(size)
############################################

# class to store all the sitting blocks


class Block_List:
    d = {}  # dictionary to hold sitting blocks' positions and themselves in "(x,y):block" fashion

    def draw_all(self, surface):
        for block in self.d.values():
            block.draw(surface)

    def append(self, b):
        self.d[b.block.topleft] = b

    def clear_row(self):
        count = 0
        for i in range(row):
            for j in range(col):
                if (j * block_size, i * block_size) in self.d:
                    count += 1
            if count == col:
                for c in range(col):
                    del self.d[(c * block_size, i * block_size)]
            count = 0


class Block(Rect):
    def __init__(self):
        self.block = Rect(0, block_size, block_size, block_size)

    def collide_down(self, d):
        if self.block.bottomleft in d:
            return True
        return False

    # def collide_left(self, l):

    def key_press(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.block.move_ip(-block_size, 0)
        if key[pygame.K_RIGHT]:
            self.block.move_ip(block_size, 0)
        if key[pygame.K_UP]:
            self.block.move_ip(0, -block_size)
        if key[pygame.K_DOWN]:
            # to add instant drop function
            self.block.move_ip(0, block_size)

    def draw(self, surface):
        pygame.draw.rect(surface, color, self.block)


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
    print(block_list.d, "bottom left pos ", curr_block.block.bottomleft)

    if curr_block.block.bottom >= block_size * row or curr_block.collide_down(block_list.d):
        block_list.append(curr_block)  # add to sitting blocks then create a new block
        block_list.clear_row()
        curr_block = Block()

    curr_block.draw(screen)  # draw the falling block

    block_list.draw_all(screen)  # draw all the siting blocks

    pygame.display.flip()

pygame.quit()
