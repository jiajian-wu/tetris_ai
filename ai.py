import pygame
import random
from shape import Shape
from pygame.rect import Rect
import math
import copy
import statistics
# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

# Set the height and width of the screen
block_size = 20
row, col = 20, 10
color = BLUE
size = [block_size * (col + 6), block_size * row]
screen = pygame.display.set_mode(size)


def draw_separate_line(s):   # left, top, width, height
    pygame.draw.rect(s, BLACK, Rect(block_size * col, 0, block_size/5, block_size * row))

############################################

# class to store all the sitting blocks


class Block_List:
    # dictionary to hold sitting blocks' positions and themselves in
    # "(left,top):(block, color)" fashion
    block_dict = {}
    block_list = []
    pos_matrix = [[0] * col for i in range(row)]
    total_row_cleared = 0
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
        self.pos_matrix = [[0] * col for i in range(row)]

        for i in range(row):
            for j in range(col):
                if (j * block_size, i * block_size) in self.block_dict:
                    count += 1
            if count == col:
                for c in range(col):
                    del self.block_dict[(c * block_size, i * block_size)]
                row_cleared += 1
                self.total_row_cleared += 1
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

        self.build_pos_matrix()

        # # print to test
        # for item in self.block_list:
        #     print(item[0], end=" ")
        # self.print_pos_matrix()
        #
        # apex_list = []  # position i stores the row number of the highest block at column i.
        # for j in range(col):
        #     try:
        #         idx = [self.pos_matrix[i][j] for i in range(len(self.pos_matrix))].index(1)
        #         apex_list.append(idx)
        #     except ValueError:
        #         apex_list.append(row)
        # print("the list contains the apexes: ")
        # print(apex_list)

    def build_pos_matrix(self):
        for pos in self.block_dict:
            self.pos_matrix[int(pos[1]/block_size)][int(pos[0]/block_size)] = 1

    def print_pos_matrix(self):
        print("\nThe position matrix is:")
        for r in self.pos_matrix:
            print(r)
        print("\n")


class Block(Rect):

    def __init__(self, matrix):
        self.shape = []     # list to hold blocks which makes up the shape
        self.type = ""
        self.state = None
        self.color = random.choice([BLUE, GREEN, RED, ORANGE])
        self.curr_steps = 0
        self.right_steps = None
        draw = random.randint(1, 7)     # generate a shape
        if draw == 1:
            self.type = "I"
            # score() --> decides 1.state with best score 2.steps needed to the right
            self.score(matrix)
            if self.state == 0:
                self.block1 = Rect(0, 0, block_size, block_size)   # left, top, width, height
                self.block2 = Rect(block_size, 0, block_size, block_size)
                self.block3 = Rect(block_size * 2, 0, block_size, block_size)
                self.block4 = Rect(block_size * 3, 0, block_size, block_size)

            elif self.state == 1:
                self.block1 = Rect(0, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(0, block_size, block_size, block_size)
                self.block3 = Rect(0, block_size * 2, block_size, block_size)
                self.block4 = Rect(0, block_size * 3, block_size, block_size)

        elif draw == 2:
            self.type = "square"
            # score() --> decides 1.state with best score 2.steps needed to the right
            self.score(matrix)
            if self.state == 0:
                self.block1 = Rect(0, 0, block_size, block_size)
                self.block2 = Rect(block_size, 0, block_size, block_size)
                self.block3 = Rect(0, block_size, block_size, block_size)
                self.block4 = Rect(block_size, block_size, block_size, block_size)

        elif draw == 3:
            self.type = "z"
            # score() --> decides 1.state with best score 2.steps needed to the right
            self.score(matrix)
            if self.state == 0:
                self.block1 = Rect(0, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(block_size, 0, block_size, block_size)
                self.block3 = Rect(block_size, block_size, block_size, block_size)
                self.block4 = Rect(block_size * 2, block_size, block_size, block_size)

            elif self.state == 1:
                self.block1 = Rect(block_size, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(0, block_size, block_size, block_size)
                self.block3 = Rect(block_size, block_size, block_size, block_size)
                self.block4 = Rect(0, block_size * 2, block_size, block_size)

        elif draw == 4:
            self.type = "z_2"
            # score() --> decides 1.state with best score 2.steps needed to the right
            self.score(matrix)
            if self.state == 0:
                self.block1 = Rect(block_size, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(block_size*2, 0, block_size, block_size)
                self.block3 = Rect(0, block_size, block_size, block_size)
                self.block4 = Rect(block_size, block_size, block_size, block_size)

            elif self.state == 1:
                self.block1 = Rect(0, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(0, block_size, block_size, block_size)
                self.block3 = Rect(block_size, block_size, block_size, block_size)
                self.block4 = Rect(block_size, block_size * 2, block_size, block_size)

        elif draw == 5:
            self.type = "T"
            self.score(matrix)
            if self.state == 0:
                self.block1 = Rect(0, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(block_size, 0, block_size, block_size)
                self.block3 = Rect(block_size * 2, 0, block_size, block_size)
                self.block4 = Rect(block_size, block_size, block_size, block_size)

            elif self.state == 1:
                self.block1 = Rect(0, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(0, block_size, block_size, block_size)
                self.block3 = Rect(block_size, block_size, block_size, block_size)
                self.block4 = Rect(0, block_size * 2, block_size, block_size)

            elif self.state == 2:
                self.block1 = Rect(block_size, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(0, block_size, block_size, block_size)
                self.block3 = Rect(block_size, block_size, block_size, block_size)
                self.block4 = Rect(block_size * 2, block_size, block_size, block_size)

            elif self.state == 3:
                self.block1 = Rect(block_size, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(0, block_size, block_size, block_size)
                self.block3 = Rect(block_size, block_size, block_size, block_size)
                self.block4 = Rect(block_size, block_size * 2, block_size, block_size)

        elif draw == 6:
            self.type = "L"
            self.score(matrix)
            if self.state == 0:
                self.block1 = Rect(0, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(block_size, 0, block_size, block_size)
                self.block3 = Rect(block_size, block_size, block_size, block_size)
                self.block4 = Rect(block_size, block_size * 2, block_size, block_size)

            elif self.state == 1:
                self.block1 = Rect(0, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(block_size, 0, block_size, block_size)
                self.block3 = Rect(block_size * 2, 0, block_size, block_size)
                self.block4 = Rect(0, block_size, block_size, block_size)

            elif self.state == 2:
                self.block1 = Rect(0, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(0, block_size, block_size, block_size)
                self.block3 = Rect(0, block_size * 2, block_size, block_size)
                self.block4 = Rect(block_size, block_size * 2, block_size, block_size)

            elif self.state == 3:
                self.block1 = Rect(block_size * 2, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(0, block_size, block_size, block_size)
                self.block3 = Rect(block_size, block_size, block_size, block_size)
                self.block4 = Rect(block_size * 2, block_size, block_size, block_size)

        elif draw == 7:
            self.type = "L_2"
            self.score(matrix)
            if self.state == 0:
                self.block1 = Rect(0, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(block_size, 0, block_size, block_size)
                self.block3 = Rect(0, block_size, block_size, block_size)
                self.block4 = Rect(0, block_size * 2, block_size, block_size)

            elif self.state == 1:
                self.block1 = Rect(0, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(0, block_size, block_size, block_size)
                self.block3 = Rect(block_size, block_size, block_size, block_size)
                self.block4 = Rect(block_size * 2, block_size, block_size, block_size)

            elif self.state == 2:
                self.block1 = Rect(block_size, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(block_size, block_size, block_size, block_size)
                self.block3 = Rect(0, block_size * 2, block_size, block_size)
                self.block4 = Rect(block_size, block_size * 2, block_size, block_size)

            elif self.state == 3:
                self.block1 = Rect(0, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(block_size, 0, block_size, block_size)
                self.block3 = Rect(block_size * 2, 0, block_size, block_size)
                self.block4 = Rect(block_size * 2, block_size, block_size, block_size)

        self.shape.append(self.block1)
        self.shape.append(self.block2)
        self.shape.append(self.block3)
        self.shape.append(self.block4)

    def score(self, matrix):  # matrix: pos_matrix in Block class

        matrix_copy = copy.deepcopy(matrix)

        apex_list = []  # position i stores the row number of the highest block at column i.
        for j in range(col):
            try:
                idx = [matrix[i][j] for i in range(len(matrix))].index(1)
                apex_list.append(idx)
            except ValueError:
                apex_list.append(row)

        # for each type, evaluate all possible positions of each rotation.
        # The number of moves are (rotations * right).

        # first position stores max_score, second position stores state,
        # third position stores # of right steps to take
        optimal_move = [None]*3
        max_score = float("-inf")
        shape_variants = Shape(self.type)
        # print("Type is ", self.type)
        for state in range(len(shape_variants.all_combos)):
            # print("State is ", state)
            rightmost = shape_variants.rightmost[state]
            for step_number in range(0, col - rightmost):   # steps to move right
                min_distance = math.inf
                for coord in shape_variants.pos[state]:
                    # find the minimum distance to move
                    # row number: coord[0], col number: coord[1]+step_number
                    distance = apex_list[coord[1]+step_number] - coord[0]
                    if distance < min_distance:
                        min_distance = distance

                # move them
                for coord in shape_variants.pos[state]:
                    matrix_copy[coord[0] + min_distance - 1][coord[1] + step_number] = 1

                score = self.score_matrix(matrix_copy, min_distance)

                # print("\nMatrix after one possible movement is: ")
                # for r in matrix_copy:
                #     print(r)
                # print("\n")

                matrix_copy = copy.deepcopy(matrix)

                if score > max_score:
                    max_score = score
                    optimal_move[0] = max_score
                    optimal_move[1] = state
                    optimal_move[2] = step_number

        self.state = optimal_move[1]
        self.right_steps = optimal_move[2]

    def score_matrix(self, matrix, move_distance):
        score = 0
        row_cleared = 0
        for r in matrix:
            if set(r) == {1}:
                row_cleared += 1
        score += row_cleared * row_cleared

        score_off = 0
        for i in range(row - 1):
            for j in range(col):
                if matrix[i][j] == 1:
                    try:
                        for k in range(i+1, row):
                            if matrix[k][j] == 1:
                                break
                            if matrix[k][j] == 0:
                                score_off += 1
                    except:
                        pass
        print("score off: ", score_off)
        score -= score_off

        apex_list = []  # position i stores the row number of the highest block at column i.
        for j in range(col):
            try:
                idx = [matrix[i][j] for i in range(len(matrix))].index(1)
                apex_list.append(idx)
            except ValueError:
                apex_list.append(row)
        apex_list = [row - i for i in apex_list]
        std = statistics.stdev(apex_list)
        print("std is ", std)
        score -= std

        return score

    def move_down(self):
        # move right to desirable position calculated by score function
        if self.curr_steps < self.right_steps:
            for item in self.shape:
                item.move_ip(block_size, 0)
            self.curr_steps += 1

        for item in self.shape:
            item.move_ip(0, block_size)

    # controlled by key_press
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
    #     if self.type == "I":
    #         step = random.randint(1, col-4)
    #     if curr_step != step:
    #         for item in self.shape:
    #             item.move_ip(block_size, 0)
    #             self.step !=


done = False
clock = pygame.time.Clock()

block_list = Block_List()
curr_block = Block(block_list.pos_matrix)

cleared_rows = pygame.font.SysFont('Arial', 30)


while not done:

    clock.tick(20)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    screen.fill(WHITE)

    # curr_block.key_press(block_list.block_dict)
    curr_block.move_down()

    if curr_block.get_bottom() >= block_size * row or curr_block.collide_down(block_list.block_dict):
        block_list.append(curr_block, curr_block.color)  # add to sitting blocks then create a new block
        block_list.clear_row()
        curr_block = Block(block_list.pos_matrix)

    curr_block.draw(screen)  # draw the falling block
    block_list.draw_all(screen)     # draw the sitting blocks
    draw_separate_line(screen)

    text_surface = cleared_rows.render(str(block_list.total_row_cleared), False, (0, 0, 0))
    screen.blit(text_surface, ((col+1) * block_size, block_size))

    pygame.display.flip()

pygame.quit()
