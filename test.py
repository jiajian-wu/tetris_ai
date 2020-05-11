# Import a library of functions called 'pygame'
import pygame
import random
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
block_size = 30
row, col = 12, 9
color = BLUE
size = [block_size * col, block_size * row]
screen = pygame.display.set_mode(size)
############################################

# class to store all the sitting blocks


class Block_List:
    d = {}  # dictionary to hold sitting blocks' positions and themselves in "(x,y):block" fashion

    def draw_all(self, surface):
        for block in self.d.values():
            pygame.draw.rect(surface, color, block)

    def append(self, b):
        for item in b.shape:
            self.d[item.topleft] = item

    def clear_row(self):
        count = 0
        row_cleared = 0
        top_cleared_row = 10000
        for i in range(row):
            for j in range(col):
                if (j * block_size, i * block_size) in self.d:
                    count += 1
            if count == col:
                for c in range(col):
                    del self.d[(c * block_size, i * block_size)]
                row_cleared += 1
                if i < top_cleared_row:
                    top_cleared_row = i
            count = 0
        # print("\nthis position above should move: ", top_cleared_row * block_size)

        block_list = self.d.items()
        block_list = sorted(block_list, key=lambda x: x[0][1], reverse=True)

        if row_cleared != 0:
            for item in block_list:     # item[0] stores the positions, item[1] stores the actual rectangle
                if item[0][1] < block_size * top_cleared_row:
                    self.d[item[0]].move_ip(0, block_size * row_cleared)    # move the rectangle
                    self.d[item[1].topleft] = item[1]   # reassign new positions
                    del self.d[item[0]]     # delete old one
        # if row_cleared != 0:
        #     for pos, piece in list(self.d.items()):
        #         if pos[1] < block_size * top_cleared_row:
        #             piece.move_ip(0, block_size * row_cleared)
        #             self.d[piece.topleft] = piece
        #             del self.d[pos]


class Block(Rect):
    def __init__(self):
        self.shape = []     # list to hold blocks which makes up the shape
        self.type = ""
        draw = random.randint(1, 2)
        if draw == 1 or draw == 2:
            self.type = "I"
            self.state = 1
            self.block1 = Rect(block_size, 0, block_size, block_size)   # left, top, width, height
            self.block2 = Rect(block_size * 2, 0, block_size, block_size)
            self.block3 = Rect(block_size * 3, 0, block_size, block_size)
            self.block4 = Rect(block_size * 4, 0, block_size, block_size)
        # elif draw == 2:
        #     self.type = "square"
        #     self.block1 = Rect(block_size, 0, block_size, block_size)
        #     self.block2 = Rect(block_size * 2, 0, block_size, block_size)
        #     self.block3 = Rect(block_size, block_size, block_size, block_size)
        #     self.block4 = Rect(block_size * 2, block_size, block_size, block_size)
        self.shape.append(self.block1)
        self.shape.append(self.block2)
        self.shape.append(self.block3)
        self.shape.append(self.block4)

    def collide_down(self, d):
        for item in self.shape:
            if item.bottomleft in d:
                return True
        return False

    # def collide_left(self, l):

    def key_press(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            for item in self.shape:
                item.move_ip(-block_size, 0)

        if key[pygame.K_RIGHT]:
            for item in self.shape:
                item.move_ip(block_size, 0)

        if key[pygame.K_DOWN]:
            for item in self.shape:
                item.move_ip(0, block_size)

        if key[pygame.K_UP]:
            self.rotate()

    def rotate(self):
        if self.type == "I":
            if self.state == 1:
                self.block1.move_ip(block_size, -block_size * 2)
                self.block2.move_ip(0, -block_size)
                self.block3.move_ip(-block_size, 0)
                self.block4.move_ip(-block_size * 2, block_size)
                self.state = 2
            else:
                self.block1.move_ip(-block_size, block_size*2)
                self.block2.move_ip(0, block_size)
                self.block3.move_ip(block_size, 0)
                self.block4.move_ip(block_size*2, -block_size)
                self.state = 1
        elif self.type == "square":
            pass

    def draw(self, surface):
        for item in self.shape:
            pygame.draw.rect(surface, color, item)

    def get_bottom(self):
        return self.block4.bottom


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

    if curr_block.get_bottom() >= block_size * row or curr_block.collide_down(block_list.d):
        block_list.append(curr_block)  # add to sitting blocks then create a new block
        block_list.clear_row()
        curr_block = Block()

    curr_block.draw(screen)  # draw the falling block

    block_list.draw_all(screen)

    pygame.display.flip()

pygame.quit()
