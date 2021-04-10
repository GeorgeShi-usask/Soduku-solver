import pygame as pg
import time
from main import Sudoku


class GameBoard:
    def __init__(self, board, rows, cols, width, height):
        self.board = board
        self.rows = rows
        self.cols = cols
        self.cells = [[Cell(self.board[i][j], i, j, width, height) for j in range(cols)]
                      for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    


class Cell:

    def __init__(self):
        self.value = None