import pygame
from .define import RED, BLACK, ROWS, COLS, BLOCK_SIZE
from .horse import Horse

class Board:
    def __init__(self):
        self.red = self.black = 12
        self.red_king = self.black_king = 0
        self.create_board()
    
    def create_board(self):

