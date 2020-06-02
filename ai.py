import pygame
import pygame.freetype
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
block_size = 15
row, col = 20, 10
color = BLUE
size = [block_size * (col + 6), block_size * row]
screen = pygame.display.set_mode(size)


def draw_separate_line(s):  # left, top, width, height
    pygame.draw.rect(s, BLACK, Rect(block_size * col, 0, block_size / 5, block_size * row))


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
        numbers_row_cleared = 0
        top_cleared_row = None
        self.pos_matrix = [[0] * col for i in range(row)]
        rows_cleared = []

        for i in range(row):
            for j in range(col):
                if (j * block_size, i * block_size) in self.block_dict:
                    count += 1
            if count == col:
                for c in range(col):
                    del self.block_dict[(c * block_size, i * block_size)]
                numbers_row_cleared += 1
                self.total_row_cleared += 1
                rows_cleared.append(i)  # record number of the row to be cleared
            count = 0
        rows_cleared = sorted(rows_cleared, reverse=True)

        # To move the rows, if any, between cleared rows
        count = 1
        for idx in range(len(rows_cleared) - 1):
            if rows_cleared[idx] - 1 == rows_cleared[idx + 1]:
                count += 1
            else:
                for mid_row in range(rows_cleared[idx] - 1, rows_cleared[idx + 1], -1):
                    try:
                        self.move(mid_row, count)
                    except:
                        pass

        if numbers_row_cleared != 0:
            top_cleared_row = rows_cleared[-1]
        self.block_list = self.block_dict.items()
        self.block_list = sorted(self.block_list, key=lambda x: x[0][1], reverse=True)
        if numbers_row_cleared != 0:
            for item in self.block_list:
                if item[0][1] < block_size * top_cleared_row:
                    self.block_dict[item[0]][0].move_ip(0, block_size * numbers_row_cleared)  # move the rectangle
                    self.block_dict[item[1][0].topleft] = self.block_dict[item[0]]  # reassign new positions
                    del self.block_dict[item[0]]  # delete old one

        self.block_list = self.block_dict.items()
        self.block_list = sorted(self.block_list, key=lambda x: x[0][1], reverse=True)

        self.build_pos_matrix()

    def move(self, mid_row, steps_to_move):
        # block_dict -> (left,top):(block, color)
        # item -> (left, top)
        for coord in self.block_dict:
            if coord[1] == mid_row * block_size:
                self.block_dict[coord][0].move_ip(0, block_size * steps_to_move)  # move the rectangle
                new_coord = self.block_dict[coord][0].topleft
                self.block_dict[new_coord] = (
                    self.block_dict[coord][0], self.block_dict[coord][1])  # reassign new positions
                del self.block_dict[coord]  # delete old one

        # # move the blocks down after row-clearing
        # # create a list from dict since dict can't keep track of order of positions.
        # self.block_list = self.block_dict.items()
        # self.block_list = sorted(self.block_list, key=lambda x: x[0][1], reverse=True)
        # if numbers_row_cleared != 0:
        #     for item in self.block_list:
        #         if item[0][1] < block_size * top_cleared_row:
        #             self.block_dict[item[0]][0].move_ip(0, block_size * numbers_row_cleared)    # move the rectangle
        #             self.block_dict[item[1][0].topleft] = (item[1][0], item[1][1])  # reassign new positions
        #             del self.block_dict[item[0]]    # delete old one
        #
        # self.block_list = self.block_dict.items()
        # self.block_list = sorted(self.block_list, key=lambda x: x[0][1], reverse=True)
        #
        # self.build_pos_matrix()

    def build_pos_matrix(self):
        for pos in self.block_dict:
            self.pos_matrix[int(pos[1] / block_size)][int(pos[0] / block_size)] = 1

    def print_pos_matrix(self):
        print("\nThe position matrix is:")
        for r in self.pos_matrix:
            print(r)
        print("\n")


class Block(Rect):

    def __init__(self, matrix):
        self.shape = []  # list to hold blocks which makes up the shape
        self.type = ""
        self.state = None
        self.color = random.choice([BLUE, GREEN, RED, ORANGE])
        self.curr_steps = 0
        self.steps = None
        self.starting_column = 4
        starting_left_pos = 4 * block_size
        draw = random.randint(1, 7)  # generate a shape
        if draw == 1:
            self.type = "I"
            # score() --> decides 1.state with best score 2.steps needed to the right
            self.score(matrix)
            if self.state == 0:
                self.block1 = Rect(starting_left_pos, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(starting_left_pos + block_size, 0, block_size, block_size)
                self.block3 = Rect(starting_left_pos + block_size * 2, 0, block_size, block_size)
                self.block4 = Rect(starting_left_pos + block_size * 3, 0, block_size, block_size)

            elif self.state == 1:
                self.block1 = Rect(starting_left_pos, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(starting_left_pos, block_size, block_size, block_size)
                self.block3 = Rect(starting_left_pos, block_size * 2, block_size, block_size)
                self.block4 = Rect(starting_left_pos, block_size * 3, block_size, block_size)

        elif draw == 2:
            self.type = "square"
            # score() --> decides 1.state with best score 2.steps needed to the right
            self.score(matrix)
            if self.state == 0:
                self.block1 = Rect(starting_left_pos, 0, block_size, block_size)
                self.block2 = Rect(starting_left_pos + block_size, 0, block_size, block_size)
                self.block3 = Rect(starting_left_pos, block_size, block_size, block_size)
                self.block4 = Rect(starting_left_pos + block_size, block_size, block_size, block_size)

        elif draw == 3:
            self.type = "z"
            # score() --> decides 1.state with best score 2.steps needed to the right
            self.score(matrix)
            if self.state == 0:
                self.block1 = Rect(starting_left_pos + 0, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(starting_left_pos + block_size, 0, block_size, block_size)
                self.block3 = Rect(starting_left_pos + block_size, block_size, block_size, block_size)
                self.block4 = Rect(starting_left_pos + block_size * 2, block_size, block_size, block_size)

            elif self.state == 1:
                self.block1 = Rect(starting_left_pos + block_size, 0, block_size,
                                   block_size)  # left, top, width, height
                self.block2 = Rect(starting_left_pos + 0, block_size, block_size, block_size)
                self.block3 = Rect(starting_left_pos + block_size, block_size, block_size, block_size)
                self.block4 = Rect(starting_left_pos + 0, block_size * 2, block_size, block_size)

        elif draw == 4:
            self.type = "z_2"
            # score() --> decides 1.state with best score 2.steps needed to the right
            self.score(matrix)
            if self.state == 0:
                self.block1 = Rect(starting_left_pos + block_size, 0, block_size,
                                   block_size)  # left, top, width, height
                self.block2 = Rect(starting_left_pos + block_size * 2, 0, block_size, block_size)
                self.block3 = Rect(starting_left_pos + 0, block_size, block_size, block_size)
                self.block4 = Rect(starting_left_pos + block_size, block_size, block_size, block_size)

            elif self.state == 1:
                self.block1 = Rect(starting_left_pos + 0, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(starting_left_pos + 0, block_size, block_size, block_size)
                self.block3 = Rect(starting_left_pos + block_size, block_size, block_size, block_size)
                self.block4 = Rect(starting_left_pos + block_size, block_size * 2, block_size, block_size)

        elif draw == 5:
            self.type = "T"
            self.score(matrix)
            if self.state == 0:
                self.block1 = Rect(starting_left_pos + 0, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(starting_left_pos + block_size, 0, block_size, block_size)
                self.block3 = Rect(starting_left_pos + block_size * 2, 0, block_size, block_size)
                self.block4 = Rect(starting_left_pos + block_size, block_size, block_size, block_size)

            elif self.state == 1:
                self.block1 = Rect(starting_left_pos + 0, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(starting_left_pos + 0, block_size, block_size, block_size)
                self.block3 = Rect(starting_left_pos + block_size, block_size, block_size, block_size)
                self.block4 = Rect(starting_left_pos + 0, block_size * 2, block_size, block_size)

            elif self.state == 2:
                self.block1 = Rect(starting_left_pos + block_size, 0, block_size,
                                   block_size)  # left, top, width, height
                self.block2 = Rect(starting_left_pos + 0, block_size, block_size, block_size)
                self.block3 = Rect(starting_left_pos + block_size, block_size, block_size, block_size)
                self.block4 = Rect(starting_left_pos + block_size * 2, block_size, block_size, block_size)

            elif self.state == 3:
                self.block1 = Rect(starting_left_pos + block_size, 0, block_size,
                                   block_size)  # left, top, width, height
                self.block2 = Rect(starting_left_pos + 0, block_size, block_size, block_size)
                self.block3 = Rect(starting_left_pos + block_size, block_size, block_size, block_size)
                self.block4 = Rect(starting_left_pos + block_size, block_size * 2, block_size, block_size)

        elif draw == 6:
            self.type = "L"
            self.score(matrix)
            if self.state == 0:
                self.block1 = Rect(starting_left_pos + 0, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(starting_left_pos + block_size, 0, block_size, block_size)
                self.block3 = Rect(starting_left_pos + block_size, block_size, block_size, block_size)
                self.block4 = Rect(starting_left_pos + block_size, block_size * 2, block_size, block_size)

            elif self.state == 1:
                self.block1 = Rect(starting_left_pos + 0, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(starting_left_pos + block_size, 0, block_size, block_size)
                self.block3 = Rect(starting_left_pos + block_size * 2, 0, block_size, block_size)
                self.block4 = Rect(starting_left_pos + 0, block_size, block_size, block_size)

            elif self.state == 2:
                self.block1 = Rect(starting_left_pos + 0, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(starting_left_pos + 0, block_size, block_size, block_size)
                self.block3 = Rect(starting_left_pos + 0, block_size * 2, block_size, block_size)
                self.block4 = Rect(starting_left_pos + block_size, block_size * 2, block_size, block_size)

            elif self.state == 3:
                self.block1 = Rect(starting_left_pos + block_size * 2, 0, block_size,
                                   block_size)  # left, top, width, height
                self.block2 = Rect(starting_left_pos + 0, block_size, block_size, block_size)
                self.block3 = Rect(starting_left_pos + block_size, block_size, block_size, block_size)
                self.block4 = Rect(starting_left_pos + block_size * 2, block_size, block_size, block_size)

        elif draw == 7:
            self.type = "L_2"
            self.score(matrix)
            if self.state == 0:
                self.block1 = Rect(starting_left_pos + 0, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(starting_left_pos + block_size, 0, block_size, block_size)
                self.block3 = Rect(starting_left_pos + 0, block_size, block_size, block_size)
                self.block4 = Rect(starting_left_pos + 0, block_size * 2, block_size, block_size)

            elif self.state == 1:
                self.block1 = Rect(starting_left_pos + 0, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(starting_left_pos + 0, block_size, block_size, block_size)
                self.block3 = Rect(starting_left_pos + block_size, block_size, block_size, block_size)
                self.block4 = Rect(starting_left_pos + block_size * 2, block_size, block_size, block_size)

            elif self.state == 2:
                self.block1 = Rect(starting_left_pos + block_size, 0, block_size,
                                   block_size)  # left, top, width, height
                self.block2 = Rect(starting_left_pos + block_size, block_size, block_size, block_size)
                self.block3 = Rect(starting_left_pos + 0, block_size * 2, block_size, block_size)
                self.block4 = Rect(starting_left_pos + block_size, block_size * 2, block_size, block_size)

            elif self.state == 3:
                self.block1 = Rect(starting_left_pos + 0, 0, block_size, block_size)  # left, top, width, height
                self.block2 = Rect(starting_left_pos + block_size, 0, block_size, block_size)
                self.block3 = Rect(starting_left_pos + block_size * 2, 0, block_size, block_size)
                self.block4 = Rect(starting_left_pos + block_size * 2, block_size, block_size, block_size)

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
        # third position stores # of steps to take
        optimal_move = [None] * 3
        max_score = float("-inf")
        shape_variants = Shape(self.type)
        # print("Type is ", self.type)
        for state in range(len(shape_variants.all_combos)):
            # print("State is ", state)
            rightmost = shape_variants.rightmost[state] + self.starting_column
            for step_number in range(0, col - rightmost):  # steps to move RIGHT
                min_distance = math.inf
                for coord in shape_variants.pos[state]:
                    # find the minimum distance to move
                    # row number: coord[0], col number: coord[1]+step_number
                    distance = apex_list[coord[1] + step_number + self.starting_column] - coord[0]
                    if distance < min_distance:
                        min_distance = distance

                # move them
                for coord in shape_variants.pos[state]:
                    matrix_copy[coord[0] + min_distance - 1][coord[1] + step_number + self.starting_column] = 1

                score = self.score_matrix(matrix_copy, min_distance)

                # print("\nMatrix after one possible movement is: ")
                # for idx, r in enumerate(matrix_copy):
                #     print(f'{idx: > 5}', r)
                # print("\n")

                matrix_copy = copy.deepcopy(matrix)

                if score > max_score:
                    max_score = score
                    optimal_move[0] = max_score
                    optimal_move[1] = state
                    optimal_move[2] = step_number

            for step_number in range(-1, -(self.starting_column + 1), -1):  # steps to move LEFT
                min_distance = math.inf
                for coord in shape_variants.pos[state]:
                    # find the minimum distance to move
                    # row number: coord[0], col number: coord[1] + step_number + starting_column
                    distance = apex_list[coord[1] + step_number + self.starting_column] - coord[0]
                    if distance < min_distance:
                        min_distance = distance

                # move them
                for coord in shape_variants.pos[state]:
                    matrix_copy[coord[0] + min_distance - 1][coord[1] + step_number + self.starting_column] = 1

                score = self.score_matrix(matrix_copy, min_distance)

                # print("\nMatrix after one possible movement is: ")
                # for idx, r in enumerate(matrix_copy):
                #     print(f'{idx: > 5}', r)
                # print("\n")

                matrix_copy = copy.deepcopy(matrix)

                if score > max_score:
                    max_score = score
                    optimal_move[0] = max_score
                    optimal_move[1] = state
                    optimal_move[2] = step_number

        self.state = optimal_move[1]
        self.steps = optimal_move[2]

    def score_matrix(self, matrix, move_distance):
        score = 0
        row_cleared = 0
        for r in matrix:
            if set(r) == {1}:
                row_cleared += 1
        score += row_cleared * row_cleared

        landing_height = row - move_distance
        score -= landing_height

        holes = 0
        for i in range(row - 1):
            for j in range(col):
                if matrix[i][j] == 1:
                    try:
                        for k in range(i + 1, row):
                            if matrix[k][j] == 1:
                                break
                            if matrix[k][j] == 0:
                                holes += 1
                    except:
                        pass
        # print("# of holes: ", holes)
        score -= 4 * holes

        # cumulative well (a well with depth N will have 1+2+3+...+N score)
        well_sum = 0

        depth = 0
        for i in range(row):
            if matrix[i][0] == 0 and matrix[i][1] == 1:
                depth += 1
                well_sum += depth
            if matrix[i][0] == 1:
                depth = 0

        depth = 0
        for i in range(row):
            if matrix[i][col - 1] == 0 and matrix[i][col - 2] == 1:
                depth += 1
                well_sum += depth
            if matrix[i][col - 1] == 1:
                depth = 0

        for c in range(1, col - 1):
            depth = 0
            for r in range(row):
                if matrix[r][c] == 0 and matrix[r][c - 1] == 1 and matrix[r][c + 1] == 1:
                    depth += 1
                    well_sum += depth
                else:
                    depth = 0
        score -= well_sum
        # if well_sum > 10:
        #     print("Well sum: ", well_sum, "\nMatrix: ")
        #     for r in matrix:
        #         print(r)
        #     print("\n")

        #########################################################
        # Row Transition #
        row_transition = 0
        for r in range(row):
            if 1 in matrix[r]:
                state = 1
                for c in range(col):
                    if matrix[r][c] == 0:
                        curr_state = 0
                        if curr_state != state:
                            state = curr_state
                            row_transition += 1
                        if c == col - 1:
                            row_transition += 1
                    elif matrix[r][c] == 1:
                        curr_state = 1
                        if curr_state != state:
                            state = curr_state
                            row_transition += 1
                # print(r, "cumulative transition: ", row_transition)
        score -= row_transition
        # print("row_transition is ", row_transition, "\nMatrix: ")
        # for row_idx, r in enumerate(matrix):
        #     print(f'{row_idx:>5}', ": ", r)
        # print("\n")
        #####################################################

        #####################################################
        # Column Transition #
        col_transition = 0
        for c in range(col):
            state = 0
            for r in range(row):
                if matrix[r][c] == 1:
                    curr_state = 1
                    if curr_state != state:
                        state = curr_state
                        col_transition += 1
                elif matrix[r][c] == 0:
                    curr_state = 0
                    if curr_state != state:
                        state = curr_state
                        col_transition += 1
                    if r == row - 1:
                        col_transition += 1
        score -= col_transition
        #####################################################
        # print("cumulative col_transition is ", col_transition, "\nMatrix: ")
        # for row_idx, r in enumerate(matrix):
        #     print(f'{row_idx:>5}', ": ", r)
        # print("\n")

        score -= col_transition

        return score

    def move_down(self):
        # move left or right to desirable position calculated by score function
        if self.steps < 0:  # moving left
            if self.curr_steps > self.steps:
                for item in self.shape:
                    item.move_ip(-block_size, 0)
                self.curr_steps -= 1
        elif self.steps > 0:  # moving right
            if self.curr_steps < self.steps:
                for item in self.shape:
                    item.move_ip(block_size, 0)
                self.curr_steps += 1

        # move down
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
                self.block1.move_ip(-block_size, block_size * 2)
                self.block2.move_ip(0, block_size)
                self.block3.move_ip(block_size, 0)
                self.block4.move_ip(block_size * 2, -block_size)
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


done = False
clock = pygame.time.Clock()

block_list = Block_List()
curr_block = Block(block_list.pos_matrix)

font = pygame.freetype.SysFont('Arial', 20)

while not done:

    clock.tick(100)

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
    block_list.draw_all(screen)  # draw the sitting blocks
    draw_separate_line(screen)  # draw right edge

    font.render_to(screen, ((col + 2) * block_size, block_size * 2),
                   str(block_list.total_row_cleared), (0, 0, 0))

    pygame.display.flip()

pygame.quit()
