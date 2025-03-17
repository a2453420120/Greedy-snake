import pygame
from constants import *

def draw_snake(block, snake_list, display):
    for x in snake_list:
        pygame.draw.rect(display, BLACK, [x[0], x[1], block, block])