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
ORANGE = (255, 165, 0)

# Set the height and width of the screen
block_size = 30
row, col = 25, 9
color = BLUE
size = [block_size * col, block_size * row]
screen = pygame.display.set_mode(size)

############################################

# class to store all the sitting blocks


class Block_List:
    # dictionary to hold sitting blocks' positions and themselves in
    # "(left,top):(block, color)" fashion
    block_dict = {}
    block_list = []
    pos_matrix = [[0] * col] * row     # [[0]*10]*10
    # def find_curr_top(self):    # find top position

    def draw_all(self, surface):
        for pos, key in self.block_dict.items():
            pygame.draw.rect(surface, key[1], key[0])

    def append(self, b, c):
        for item in b.shape:
            self.block_dict[item.topleft] = (item, c)

    def clear_row(self):
        count = 0
        row_cleared = 0
        top_cleared_row = 10000
        for i in range(row):
            for j in range(col):
                if (j * block_size, i * block_size) in self.block_dict:
                    count += 1
            if count == col:
                for c in range(col):
                    del self.block_dict[(c * block_size, i * block_size)]
                row_cleared += 1
                if i < top_cleared_row:
                    top_cleared_row = i
            count = 0

        # move the blocks down after row-clearing
        # create a list from dict since dict can't keep track of order of positions.
        self.block_list = self.block_dict.items()
        self.block_list = sorted(self.block_list, key=lambda x: x[0][1], reverse=True)
        if row_cleared != 0:
            for item in self.block_list:
                if item[0][1] < block_size * top_cleared_row:
                    self.block_dict[item[0]][0].move_ip(0, block_size * row_cleared)    # move the rectangle
                    self.block_dict[item[1][0].topleft] = (item[1][0], item[1][1])  # reassign new positions
                    del self.block_dict[item[0]]    # delete old one

        self.block_list = self.block_dict.items()
        self.block_list = sorted(self.block_list, key=lambda x: x[0][1], reverse=True)
        for item in self.block_list:
            print(item[0], end=" ")
        print(self.pos_matrix)
        print("\n")

    # def print_pos_matrix(self):


class Block(Rect):
    def __init__(self):
        self.shape = []     # list to hold blocks which makes up the shape
        self.type = ""
        self.color = random.choice([BLUE, GREEN, RED, ORANGE])
        draw = random.randint(1, 2)
        if draw == 1:
            self.type = "I"
            self.state = 1
            self.block1 = Rect(block_size, 0, block_size, block_size)   # left, top, width, height
            self.block2 = Rect(block_size * 2, 0, block_size, block_size)
            self.block3 = Rect(block_size * 3, 0, block_size, block_size)
            self.block4 = Rect(block_size * 4, 0, block_size, block_size)
        elif draw == 2:
            self.type = "square"
            self.block1 = Rect(block_size, 0, block_size, block_size)
            self.block2 = Rect(block_size * 2, 0, block_size, block_size)
            self.block3 = Rect(block_size, block_size, block_size, block_size)
            self.block4 = Rect(block_size * 2, block_size, block_size, block_size)

        self.shape.append(self.block1)
        self.shape.append(self.block2)
        self.shape.append(self.block3)
        self.shape.append(self.block4)

        # elif draw == 3:
        #     self.type = "T"
        #     self.state = 1
        #     self.block1 = Rect(block_size, block_size, block_size, block_size)
        #     self.block2 = Rect(block_size * 2, block_size, block_size, block_size)
        #     self.block3 = Rect(block_size * 3, block_size, block_size, block_size)
        #     self.block4 = Rect(block_size * 2, 0, block_size, block_size)

    def rotate(self):
        # prohibit rotation if finished positions already occupied !!!
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

        # elif self.type == "T":
        #     if self.state == 1:

    def collide_down(self, d):
        for item in self.shape:
            if item.bottomleft in d:
                return True
        return False

    def move_left(self, d):
        clear_to_move = True
        for item in self.shape:
            if (item.topleft[0] - block_size, item.topleft[1]) in d or item.left == 0:
                clear_to_move = False
        if clear_to_move:
            for item in self.shape:
                item.move_ip(-block_size, 0)

    def move_right(self, d):
        clear_to_move = True
        for item in self.shape:
            if (item.topleft[0] + block_size, item.topleft[1]) in d or item.right == block_size * col:
                clear_to_move = False
        if clear_to_move:
            for item in self.shape:
                item.move_ip(block_size, 0)

    def move_down(self):
        for item in self.shape:
            item.move_ip(0, block_size)

    def key_press(self, d):
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            self.move_left(d)

        if key[pygame.K_RIGHT]:
            self.move_right(d)

        if key[pygame.K_UP]:
            self.rotate()

    def draw(self, surface):
        for item in self.shape:
            pygame.draw.rect(surface, self.color, item)

    def get_bottom(self):
        return self.block4.bottom

    # def move_right_test(self):
    #     for item in self.shape:
    #         if item.right != block_size * col:
    #             item.move_ip(block_size, 0)


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

    curr_block.key_press(block_list.block_dict)
    curr_block.move_down()
    # curr_block.move_right_test()

    if curr_block.get_bottom() >= block_size * row or curr_block.collide_down(block_list.block_dict):
        block_list.append(curr_block, curr_block.color)  # add to sitting blocks then create a new block
        block_list.clear_row()
        curr_block = Block()

    curr_block.draw(screen)  # draw the falling block

    block_list.draw_all(screen)

    pygame.display.flip()

pygame.quit()
