from random import sample


class Sudoku:
    def random_board(self):
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

        board = [[nums[pattern(r, c)] for c in cols] for r in rows]

        squares = side * side
        empties = squares * 3 // 4

        for p in sample(range(squares), empties):
            board[p // side][p % side] = 0

        return board

    def display(self, board):
        """
        display the generated game board
        :return:
        """
        for i in range(len(board)):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - -")

            for j in range(len(board[0])):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")
                if j == 8:
                    print(board[i][j])
                else:
                    print(str(board[i][j]) + " ", end="")

    def solve(self, board):
        """
        automatically solve the sudoku
        :return:
        """
        find = self.find_empty(board)
        if not find:
            return True
        else:
            row, col = find
            for i in range(1, 10):
                if (not self.check_row(board, find, i)) and \
                        (not self.check_col(board, find, i)) and \
                        (not self.check_square(board, find, i)):
                    board[row][col] = i
                    if self.solve(board):
                        return True
                board[row][col] = 0

        return False

    def check_row(self, board, pos, num):
        """
        check if the num has already been a part of that row
        :param pos: the position of that num
        :param num: the input num
        :return: bool, if exists, return True; else, return False
        """
        for i in range(len(board[0])):
            if board[pos[0]][i] == num and pos[1] != i:
                return True
        return False

    def check_col(self, board, pos, num):
        """
        check if the num has already been a part of that col
        :param pos: the position of that num
        :param num: the input num
        :return: bool, if exists, return True; else, return False
        """
        for i in range(len(board)):
            if board[i][pos[1]] == num and pos[0] != i:
                return True
        return False

    def check_square(self, board, pos, num):
        """
        check if the num has already been a part of that 3x3 square
        :param pos: the position of that num
        :param num: the input num
        :return: bool, if exists, return True; else, return False
        """
        # find which box the num is at
        box_col = pos[1] // 3 * 3
        box_row = pos[0] // 3 * 3

        # loop through all 9 elements in the box to check for duplicates
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num and (i, j) != pos:
                    return True
        return False

    def find_empty(self, board):
        """
        find the empty spaces in the game
        :return: a tuple of row and col of that empty space
        """
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == 0:
                    return (row, col)
        return None


sudoku = Sudoku()
board = sudoku.random_board()
sudoku.display(board)
sudoku.solve(board)
sudoku.display(board)
