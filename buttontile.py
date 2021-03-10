from tkinter import Button, PhotoImage, constants

class ButtonTile(Button):

    # consts values for button cover
    UNCOVERED: int = -1
    COVER_BLANK: int = 0
    COVER_FLAG: int = 1
    COVER_QUESTION: int = 2

    def __init__(self, top, row: int=0, col: int=0):
        self._row = row
        self._col = col
        self._uncovered_image = None
        self._blank_image = PhotoImage(file='./gifs/blank.gif')
        self._flag_image = PhotoImage(file='./gifs/flag.gif')
        self._question_image = PhotoImage(file='./gifs/question.gif')
        Button.__init__(self, top)
        self.initialize_tile()
    # end __init__

    def initialize_tile(self) -> None:
        self._cover = 0
        self._value = 0
        self.config(state=constants.NORMAL, relief=constants.RAISED, justify=constants.CENTER)
        self.config(bd=0, image=self._blank_image)
    # end initialize_tile

    def place_in_gui(self) -> None:
        self.grid(row=self._row, column=self._col)
    # end place_in_gui

    def set_row_col(self, row=0, col=0) -> None:
        self._row = row
        self._col = col
    # end place_in_gui

    def set_value(self, val: int=0) -> None: self._value = val
    def get_value(self) -> int: return self._value
    def get_row_col(self) -> tuple[int, int]: return self._row, self._col
    def get_cover(self) -> int: return self._cover

    def print_contents(self) -> None:
        print("[%d,%d]" % (self._value, self._cover), end='')
    # end print_contents

    def set_cover(self) -> None:

        if self._cover == ButtonTile.COVER_BLANK:
            self._cover = ButtonTile.COVER_FLAG
            self.config(image=self._flag_image)
        elif self._cover == ButtonTile.COVER_FLAG:
            self._cover = ButtonTile.COVER_QUESTION
            self.config(image=self._question_image)
        elif self._cover == ButtonTile.COVER_QUESTION:
            self._cover = ButtonTile.COVER_BLANK
            self.config(image=self._blank_image)
        elif self._cover == ButtonTile.UNCOVERED:
           pass

    # end set_cover

    def uncover(self) -> None:

        if self._cover == 0:
           self._cover = -1
           if self._value == 0:
               self.uncovered_image = self._blank_image
           elif self._value == 1:
               self.uncovered_image = PhotoImage(file='./gifs/one.gif')
           elif self._value == 2:
               self.uncovered_image = PhotoImage(file='./gifs/two.gif')
           elif self._value == 3:
               self.uncovered_image = PhotoImage(file='./gifs/three.gif')
           elif self._value == 4:
               self.uncovered_image = PhotoImage(file='./gifs/four.gif')
           elif self._value == 5:
               self.uncovered_image = PhotoImage(file='./gifs/five.gif')
           elif self._value == 6:
               self.uncovered_image = PhotoImage(file='./gifs/six.gif')
           elif self._value == 7:
               self.uncovered_image = PhotoImage(file='./gifs/seven.gif')
           elif self._value == 8:
               self.uncovered_image = PhotoImage(file='./gifs/eight.gif')
           elif self._value == 9:
               self.uncovered_image = PhotoImage(file='./gifs/mine.gif')

           self.config(state=constants.DISABLED, relief=constants.FLAT, image=self.uncovered_image)

    # end uncover