import pygame as pg
import time
from main import Sudoku


class GameBoard:
    def __init__(self, board, width, height):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])
        self.cells = [[Cell(self.board[i][j], i, j, width, height) for j in range(len(board[0]))]
                      for i in range(len(board))]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def update_model(self):
        self.model = [[self.cells[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cells[row][col].set(val) == 0:
            self.cells[row][col].set(val)
            self.update_model()

            if ((not Sudoku.check_row(self.model, (row, col), val)) and
                (not Sudoku.check_col(self.model, (row, col), val)) and
                (not Sudoku.check_square(self.model, (row, col), val))) and Sudoku.solve(self.model):
                return True
            else:
                self.cells[row][col].set(0)
                self.cells[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cells[row][col].set_temp(val)

    def draw(self, win):
        col_width = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pg.draw.line(win, (0, 0, 0), (0, i * col_width), (self.width, i * col_width), thick)
            pg.draw.line(win, (0, 0, 0), (i * col_width, 0), (i * col_width, self.height), thick)

        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw(win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].selected = False

        self.cells[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cells[row][col].value == 0:
            self.cells[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j].value == 0:
                    return False
        return True

class Cell:

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

