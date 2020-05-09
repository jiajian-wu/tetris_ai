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

done = False
clock = pygame.time.Clock()

blocks = []
curr_block = Rect(20, 20, 20, 20)

while not done:

    clock.tick(10)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    screen.fill(WHITE)

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        curr_block.move_ip(-10, 0)
    if key[pygame.K_RIGHT]:
        curr_block.move_ip(10, 0)
    if key[pygame.K_UP]:
        curr_block.move_ip(0, -10)
    if key[pygame.K_DOWN]:
        curr_block.move_ip(0, 10)

    if curr_block.bottom > 300 or curr_block.collidelist(blocks) != -1:
        blocks.append(curr_block)   # add to sitting blocks then create a new block
        curr_block = Rect(20, 20, 20, 20)

    pygame.draw.rect(screen, GREEN, curr_block)  # draw the falling block

    for b in blocks:
        pygame.draw.rect(screen, GREEN, b)  # draw all the siting blocks

    pygame.display.flip()

pygame.quit()
