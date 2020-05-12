"""Main module for the Sudoku game

Uses the model view controller (mvc) pattern to implement the GUI.
No ABCs are defined, rather, interfaces are implicitly defined. In
other words, the module is completly reliant on duck-typing.

Attributes:
    MARGIN: pixels around the board
    SIDE: width of every board cell
    WIDTH: width of the whole board
    HEIGHT: height of the whole board
    BUTTON_HEIGHT: height of the buttons
"""
from tkinter import Tk, Canvas, Frame, Button, TOP, BOTTOM, BOTH, LEFT, RIGHT
import copy

import algorithms as alg

MARGIN = 10
SIDE = 50
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9
BUTTON_HEIGHT = 40


class SudokuModel:
    """The model of the mvc pattern. Represents a Sudoku puzzle.

    This class is also a subject in the observer pattern

    Attrubutes:
        _observers (list): list of observers to this model which should
            only be views
    """
    def __init__(self):
        self._board = None
        self._original = None
        self._observers = []

    def add_observer(self, observer):
        """adds to the list of observers to be notified upon state change"""
        self._observers.append(observer)

    def get_board(self):
        """Get the current board"""
        return self._board
    
    def get_original(self):
        """Get the original board before modification"""
        return self._original

    def notify_observers(self):
        """Notify the observers that the state of this model has changed"""
        for view in self._observers:
            view.handle_state_change(self)
    
    def set_board(self, board):
        """Set the board
        
        Args:
            board (list): the board to which self.board will be set
        """
        self._board = board
        self.notify_observers()

    def setup(self):
        """Sets up a new game"""
        self._board = alg.generate_puzzle()
        self._original = copy.deepcopy(self._board)
        self.notify_observers()


class SudokuController:
    """The controller in the mvc pattern

    Attributes:
        model: the model
    """
    def __init__(self, model):
        self.model = model

    def new_game(self):
        self.model.setup()

    def reset(self):
        self.model.set_board(self.model.get_original())

    def solve(self):
        self.model.set_board(alg.solve(self.model.get_original()))

    def cell_clicked(self, view, event):
        x = event.x
        y = event.y

        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            event.widget.focus_set()

            row = int((y - MARGIN) / SIDE)
            col = int((x - MARGIN) / SIDE)

            if row == view.get_row() and col == view.get_col():
                view.set_row(-1)
                view.set_col(-1)
            elif self.model.get_board()[row][col] == 0:
                view.set_row(row)
                view.set_col(col)

        view.draw_cursor()

    def number_pressed():
        pass
 
 
class SudokuView(Frame):
    """A tkinter Frame that graphically represents a Sudoku puzzle

    Observer of the model in the mvc pattern. Notifies the controller
    when the user performs an action.

    Attributes:
        parent (widgit): the parent container of this Frame
        controller: a controller
    """
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        parent.minsize(height=HEIGHT + BUTTON_HEIGHT, width=WIDTH)
        parent.maxsize(height=HEIGHT, width=WIDTH)
        self.parent = parent
        self.controller = controller
        self._row = 0
        self._col = 0
        self.canvas = None # Truly initialized in helper mehtod

        self._set_layout()

    def draw_cursor(self):
        """Draw a box around the user selected area."""
        self.canvas.delete("cursor")
        if self._row >= 0 and self._col >= 0:
            x0 = MARGIN + self._col * SIDE + 1
            y0 = MARGIN + self._row * SIDE + 1
            x1 = MARGIN + (self._col + 1) * SIDE - 1
            y1 = MARGIN + (self._row + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1, outline="red", tags="cursor")

    def handle_state_change(self, subject):
        board = subject.get_board()
        original = subject.get_original()
        self._draw_puzzle(board, original)

    def get_row(self):
        return self._row

    def get_col(self):
        return self._col

    def set_row(self, row):
        self._row = row

    def set_col(self, col):
        self._col = col

    def _set_layout(self):
        # Set the layout of the board UI.
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        self.canvas.config(highlightthickness=0)

        button_panel = Frame(self)
        button_panel.pack(fill=BOTH, side=BOTTOM)
        button = Button(button_panel, text="Reset", command=self.controller.reset)
        button.pack(side=RIGHT)
        button = Button(button_panel, text="New Game", command=self.controller.new_game)
        button.pack(side=RIGHT)
        button = Button(button_panel, text="Solve", command=self.controller.solve)
        button.pack(side=LEFT)
        self.canvas.bind(
                "<Button-1>", lambda event :
                self.controller.cell_clicked(self, event))
        self.canvas.bind("<Key>", self._key_pressed)

        self._draw_grid()
        #self._draw_puzzle()

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

    def _draw_puzzle(self, board, original):
        # Draw the puzzle values onto the UI.
        self.canvas.delete("numbers")
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

    def _key_pressed(self, event):
        if self.row >= 0 and self.col >= 0 and event.char in "0123456789":
            self.puzzle.get_board()[self.row][self.col] = int(event.char)
            self.row = -1
            self.col = -1
            self._draw_puzzle()
            self._draw_cursor()


def main():
    model = SudokuModel()
    controller = SudokuController(model)

    root = Tk()
    view = SudokuView(root, controller)
    model.add_observer(view)
    model.setup()
    root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
    root.title("Sudoku")
    root.mainloop()


if __name__ == "__main__":
    main()

