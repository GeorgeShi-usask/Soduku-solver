import pygame as pg
import time
from main import Sudoku


sudoku = Sudoku()


class GameBoard:
    def __init__(self, board, width, height, win):
        self.model = board
        self.rows = len(board)
        self.cols = len(board[0])
        self.cells = [[Cell(self.model[i][j], i, j, width, height) for j in range(len(board[0]))]
                      for i in range(len(board))]
        self.width = width
        self.height = height

        self.selected = None
        self.win = win

    def update_model(self):
        self.model = [[self.cells[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        """
        place the val in the cells, if place,
        the val can't be changed or deleted
        :param val:
        :return:
        """
        row, col = self.selected
        if self.cells[row][col].value == 0:
            self.cells[row][col].set(val)
            self.update_model()

    def sketch(self, val):
        """
        sketch the temp val to the cells on the board
        temp val can be changed or deleted
        :param val:
        :return:
        """
        row, col = self.selected
        self.cells[row][col].set_temp(val)

    def draw(self):
        """
        function to draw the board
        :return:
        """
        interval = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pg.draw.line(self.win, (0, 0, 0), (0, i * interval), (self.width, i * interval), thick)
            pg.draw.line(self.win, (0, 0, 0), (i * interval, 0), (i * interval, self.height), thick)

        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw(self.win)

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

    def solve(self):
        self.update_model()
        find = sudoku.find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find
            for i in range(1, 10):
                if (not sudoku.check_row(self.model, find, i)) and \
                        (not sudoku.check_col(self.model, find, i)) and \
                        (not sudoku.check_square(self.model, find, i)):
                    self.model[row][col] = i
                    self.cells[row][col].set(i)
                    self.cells[row][col].draw_change(self.win, True)
                    self.update_model()
                    pg.display.update()
                    pg.time.delay(100)

                    if self.solve():
                        return True

                    self.model[row][col] = 0
                    self.cells[row][col].set(0)
                    self.update_model()
                    self.cells[row][col].draw_change(self.win, False)
                    pg.display.update()
                    pg.time.delay(100)

        return False

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

    def draw(self, win):
        fnt = pg.font.SysFont("comicsans", 40)
        interval = self.width / 9
        x = self.col * interval
        y = self.row * interval

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (interval / 2 - text.get_width() / 2), y + (interval / 2 - text.get_height() / 2)))

        if self.selected:
            pg.draw.rect(win, (255, 0, 0), (x, y, interval, interval), 3)

    def draw_change(self, win, g=True):
        fnt = pg.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pg.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pg.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pg.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


pg.font.init()


def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60
    mat = " " + str(hour) + ":" + str(minute) + ":" + str(sec)
    return mat


def redraw(win, board, time):
    win.fill((255, 255, 255))

    fnt = pg.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0, 0, 0))
    win.blit(text, (350, 560))

    board.draw()


def main():
    win = pg.display.set_mode((540, 600))
    pg.display.set_caption("Sudoku")
    board = sudoku.random_board()
    gameboard = GameBoard(board, 540, 540, win)
    key = None
    run = True
    start = time.time()
    while run:

        play_time = round(time.time() - start)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    key = 1
                if event.key == pg.K_2:
                    key = 2
                if event.key == pg.K_3:
                    key = 3
                if event.key == pg.K_4:
                    key = 4
                if event.key == pg.K_5:
                    key = 5
                if event.key == pg.K_6:
                    key = 6
                if event.key == pg.K_7:
                    key = 7
                if event.key == pg.K_8:
                    key = 8
                if event.key == pg.K_9:
                    key = 9
                if event.key == pg.K_DELETE:
                    gameboard.clear()
                    key = None
                if event.key == pg.K_SPACE:
                    gameboard.solve()
                if event.key == pg.K_RETURN:
                    i, j = gameboard.selected
                    if gameboard.cells[i][j].temp != 0:
                        gameboard.place(gameboard.cells[i][j].temp)
                        key = None

                        if gameboard.is_finished():
                            print("Game over")

            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                clicked = gameboard.click(pos)
                if clicked:
                    gameboard.select(clicked[0], clicked[1])
                    key = None

        if gameboard.selected and key is not None:
            gameboard.sketch(key)

        redraw(win, gameboard, play_time)
        pg.display.update()


main()
pg.quit()
