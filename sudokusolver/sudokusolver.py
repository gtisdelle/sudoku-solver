"""Main module for the Sudoku game

Attributes:
    MARGIN: pixels around the board
    SIDE: width of every board cell
    WIDTH: width of the whole board
    HEIGHT: height of the whole board
"""
from tkinter import Tk, Canvas, Frame, Button, TOP, BOTTOM, BOTH
import copy

import algorithms as alg

MARGIN = 20
SIDE = 100
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9


class Puzzle:
    """Represents a Sudoku puzzle."""
    def __init__(self):
        """Initialize class."""
        self._board = alg.generate_puzzle()
        self.original = copy.deepcopy(self._board)
        
    def get_board(self):
        """Get the current board"""
        return self._board
    
    def get_original(self):
        """Get the original board before modification"""
        return self.original
    
    def set_board(self, board):
        """Set the board
        
        Args:
            board (list): the board to which self.board will be set
        """
        self._board = board
    
    def get_solution(self):
        """Solve the Sudoku puzzle based on the origional board.
        
        Returns:
            list: list of lists representing the solved Sudoku puzzle
        """
        return alg.solve(self._original)


class PuzzleWindow(Frame):
    """A tkinter Frame that graphically represents a Sudoku puzzle

    Attributes:
        parent (wigit): the parent container of this Frame
        puzzle (list): the list representing the Sudoku puzzle

    Authors:
        George Tisdelle
        newcoder.io
    """
    def __init__(self, parent, puzzle):
        """Initialize the attributes of this class

        Args:
            parent (wigit): the parent container of this Frame
            puzzle (list): the list representing the Sudoku puzzle
        """
        Frame.__init__(self, parent)
        self.parent = parent
        self.puzzle = puzzle
        self.row = 0
        self.col = 0
        self.canvas = None # Truly initialized in helper mehtod

        self._set_layout()

    def _set_layout(self):
        # Set the layout of the board UI.
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        reset_button = Button(self, text="Reset", command=self._reset_puzzle)
        reset_button.pack(fill=BOTH, side=BOTTOM)
        self.canvas.bind("<Button-1>", self._cell_clicked)
        self.canvas.bind("<Key>", self._key_pressed)

        self._draw_grid()
        self._draw_puzzle()

    def _draw_grid(self):
        # Draw the grid lines of the board.
        for i in range(10):
            if i % 3 == 0:
                color = "blue"
            else:
                color = "gray"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def _draw_puzzle(self):
        # Draw the puzzle values onto the UI.
        self.canvas.delete("numbers")
        board = self.puzzle.get_board()
        original = self.puzzle.get_original()
        for i in range(9):
            for j in range(9): 
                answer = board[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    generated = original[i][j]
                    if answer == generated:
                        color = "black"
                    else:
                        color = "sea green"
                    self.canvas.create_text(x, y, text=answer, tags="numbers",
                                            fill=color)

    def _reset_puzzle(self):
        # Reset the puzzle to its original state.
        self.puzzle.set_board(copy.deepcopy(self.puzzle.get_original()))
        self._draw_puzzle()

    def _cell_clicked(self, event):
        # Set the row and col attributs to the location clicked.
        x = event.x
        y = event.y

        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()

            row = int((y - MARGIN) / SIDE)
            col = int((x - MARGIN) / SIDE)

            if row == self.row and col == self.col:
                self.row = -1
                self.col = -1
            elif self.puzzle.get_board()[row][col] == 0:
                self.row = row
                self.col = col

        self._draw_cursor()

    def _draw_cursor(self):
        # Draw a box around the user selected area.
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1, outline="red", tags="cursor")

    def _key_pressed(self, event):
        if self.row >= 0 and self.col >= 0 and event.char in "0123456789":
            self.puzzle.get_board()[self.row][self.col] = int(event.char)
            self.row = -1
            self.col = -1
            self._draw_puzzle()
            self._draw_cursor()


def main():
    puzzle = Puzzle()
    root = Tk()
    PuzzleWindow(root, puzzle)
    root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
    root.mainloop()


if __name__ == "__main__":
    main()

