import pprint

import numpy


class Sudoku:
    def __init__(self):
        self.gameBoard = numpy.matrix()

        return

    def random_board(self, this):
        """
        generate a random sudoku game board
        :return:
        """
        return

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
        return

    def check_row(self, row, num):
        """
        check if the num has already been a part of that row
        :param row: the row of that num
        :param num: the input num
        :return: bool, if exists, return True; else, return False
        """
        for i in range(9):
            if self.gameBoard[row][i] == num:
                return True
        return False

    def check_col(self, col, num):
        """
        check if the num has already been a part of that col
        :param col: the col of that num
        :param num: the input num
        :return: bool, if exists, return True; else, return False
        """
        for i in range(9):
            if self.gameBoard[col][i] == num:
                return True
        return False

    def check_square(self, row, col, num):
        """
        check if the num has already been a part of that 3x3 square
        :param row: the row of that num
        :param col: the col of that num
        :param num: the input num
        :return: bool, if exists, return True; else, return False
        """
        for i in range (3):
            for j in range(3):
                if self.gameBoard[i + row][j + col] == num:
                    return True
        return False

    def find_empty(self):
        """
        find the empty spaces in the game
        :return:
        """
        for row in range(9):
            for col in range(9):
                if self.gameBoard[row][col] == 0:
                    return True
        return False

    def is_finished(self):
        """
        check if the game is finished, no more empty space
        :return:
        """

        return

