import pygame
from .define import RED, BLACK, ROWS, COLS, BLOCK_SIZE
from .horse import Horse

class Board:
    def __init__(self):
        self.board = []
        self.red = self.black = 12
        self.red_king = self.black_king = 0
        self.create_board()
    
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if(col % 2 == (row + 1) % 2):
                    if (row < 3):
                        self.board[row].append(Horse(row, col, RED))
                    elif(row > 4):
                        self.board[row].append(Horse(row, col, BLACK))
                    else:
                        self.board[row].append(0)

                else:
                    self.board[row].append(0)
