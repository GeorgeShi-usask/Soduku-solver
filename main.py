from random import sample
import pygame


class Sudoku:
    def __init__(self):
        """
        generate a random sudoku game board that can be solved
        :return:
        """
        base = 3
        side = base * base

        def pattern(r, c): return (base * (r % base) + r // base + c) % side

        def shuffle(s): return sample(s, len(s))

        rBase = range(base)
        rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
        cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
        nums = shuffle(range(1, side + 1))

        self.gameBoard = [[nums[pattern(r, c)] for c in cols] for r in rows]

        squares = side * side
        empties = squares * 3 // 4

        for p in sample(range(squares), empties):
            self.gameBoard[p // side][p % side] = 0

    def display(self):
        """
        display the generated game board
        :return:
        """
        for i in range(len(self.gameBoard)):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - -")

            for j in range(len(self.gameBoard[0])):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")
                if j == 8:
                    print(self.gameBoard[i][j])
                else:
                    print(str(self.gameBoard[i][j]) + " ", end="")

    def take_num_input(self):
        """
        function that takes in the user input number
        :return:
        """
        return

    def solve(self):
        """
        by pressing space, automatically solve the sudoku
        :return:
        """
        find = self.find_empty()
        if not find:
            return True
        else:
            row, col = find
            for i in range(1, 10):
                if (not self.check_row(find, i)) and \
                        (not self.check_col(find, i)) and \
                        (not self.check_square(find, i)):
                    self.gameBoard[row][col] = i
                    if self.solve():
                        return True
                self.gameBoard[row][col] = 0

        return False

    def check_row(self, pos, num):
        """
        check if the num has already been a part of that row
        :param pos: the position of that num
        :param num: the input num
        :return: bool, if exists, return True; else, return False
        """
        for i in range(len(self.gameBoard[0])):
            if self.gameBoard[pos[0]][i] == num and pos[1] != i:
                return True
        return False

    def check_col(self, pos, num):
        """
        check if the num has already been a part of that col
        :param pos: the position of that num
        :param num: the input num
        :return: bool, if exists, return True; else, return False
        """
        for i in range(len(self.gameBoard)):
            if self.gameBoard[i][pos[1]] == num and pos[0] != i:
                return True
        return False

    def check_square(self, pos, num):
        """
        check if the num has already been a part of that 3x3 square
        :param pos: the position of that num
        :param num: the input num
        :return: bool, if exists, return True; else, return False
        """
        # find which box the num is at
        box_col = pos[1] // 3
        box_row = pos[0] // 3

        # loop through all 9 elements in the box to check for duplicates
        for i in range(box_row * 3, box_row * 3 + 3):
            for j in range(box_col * 3, box_col * 3 + 3):
                if self.gameBoard[i][j] == num and (i, j) != pos:
                    return True
        return False

    def find_empty(self):
        """
        find the empty spaces in the game
        :return: a tuple of row and col of that empty space
        """
        for row in range(len(self.gameBoard)):
            for col in range(len(self.gameBoard[0])):
                if self.gameBoard[row][col] == 0:
                    return (row, col)
        return None


