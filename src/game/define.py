import pygame

WIDTH = 800
HEIGHT = WIDTH + (WIDTH / 2)
ROWS, COLS = 8, 8
BLOCK_SIZE = WIDTH // COLS

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)

CROWN = pygame.transform.scale(pygame.image.load('src/img/crown.png'), (44, 25))