
from tkinter import Frame, constants
from buttontile import ButtonTile
from random import  randint
from typing import List

class FieldFrame(Frame):

    # coords for adjacent tiles
    _ADJ = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
    _PERCENT_MINES = 5.0
    MINE_VALUE = 9

    def __init__(self, top, size: int=6):

        Frame.__init__(self,top, bd=5, relief=constants.RIDGE)
        self._size = size
        self._valid_flagged = 0
        self._number_of_mines = int((size**2) * (FieldFrame._PERCENT_MINES / 100 ))
        self._field_grid = {}
        self.set_field_grid()
        self.field_grid_to_gui()

    # end __init__

    def get_number_of_mines(self) -> int:
        return self._number_of_mines
    # end get_number_of_mines


    def undiscoverd_mines(self) -> int:
        return self._number_of_mines - self._valid_flagged
    # end undiscoverd_mines


    def set_field_grid(self) -> None:
        for row in range(self._size):
            for col in range(self._size):
                self._field_grid[make_name(row, col)] = ButtonTile(self, row, col)
    # end set_field_grid


    def field_grid_to_gui(self) -> None:
        for row in range(self._size):
            for col in range(self._size):
                self._field_grid[make_name(row, col)].place_in_gui()
    # end field_grid_to_gui


    def init_field_grid(self) -> None:
        for row in range(self._size):
            for col in range(self._size):
                self._field_grid[make_name(row, col)].initialize_tile()
    # end init_field_grid


    def place_mines(self) -> None:

        mine_list = []
        count: int = 0
        self._flagged: int = 0

        while count < self._number_of_mines:
            r = randint(0, (self._size**2) - 1)
            if r not in mine_list:
                mine_list.append(r)
                count += 1
            # end if
        # end while

        for a_mine in mine_list:
            row = int(a_mine / self._size)
            col = a_mine % self._size
            self.set_tile(row, col, FieldFrame.MINE_VALUE)
        # end for

    # end place_mines


    def set_adjacent(self) -> None:
        for row in range(self._size):
            for col in range(self._size):
                tile = self.get_tile(row, col)
                if(tile.get_value() != FieldFrame.MINE_VALUE):
                    sum = 0
                    for a in FieldFrame._ADJ:
                        rAdj = row + a[0]
                        cAdj = col + a[1]
                        if ((0 <= rAdj < self._size) and (0 <= cAdj < self._size)):
                            if(self.get_tile(rAdj, cAdj).get_value() == FieldFrame.MINE_VALUE):
                                sum += 1
                            # end if
                        # end if
                    # end for

                    tile.set_value(sum)

                #end if
            # end for
        #end for
    # end set_adjacent


    def show_clear_tiles(self, r: int, c: int) -> None:

        zero_cells = []
        uncovered_cells = []
        zero_cells.append((r, c))
        uncovered_cells.append((r, c))

        while len(zero_cells) != 0:
            row = zero_cells[0][0]
            col = zero_cells[0][1]
            del zero_cells[0]

            for a in FieldFrame._ADJ:
                rAdj = row + a[0]
                cAdj = col + a[1]

                if ((0 <= rAdj < self._size) and (0 <= cAdj < self._size)):
                    tile = self.get_tile(rAdj, cAdj)
                    tile.uncover()

                    if tile.get_value() == 0 and (rAdj,cAdj) not in uncovered_cells:
                        zero_cells.append((rAdj, cAdj))
                        uncovered_cells.append((rAdj, cAdj))

                    # end if
                # end if
            # end for
        # end while

    # end show_clear_tiles

    def print_contents(self) -> None:
        print("[v: 0..9, c: -1..2]")
        for row in range(self._size):
            for col in range(self._size):
                tile = self._field_grid[make_name(row, col)]
                tile.print_contents()
            print(",")
        print("undiscoverd_mines: " + str(self.undiscoverd_mines()))
    # end show_contents


    def is_game_over(self) -> bool:
        ret = False

        self._valid_flagged = 0
        # invalid_flagged: int = 0
        uncovered: int = 0

        for row in range(self._size):
            for col in range(self._size):
                tile = self._field_grid[make_name(row, col)]
                value = tile.get_value()
                cover = tile.get_cover()

                if value == FieldFrame.MINE_VALUE and cover == ButtonTile.COVER_FLAG:
                    self._valid_flagged += 1
                # end if

                # if value != FieldFrame.MINE_VALUE and cover == ButtonTile.COVER_FLAG:
                #    invalid_flagged += 1
                # end if

                if cover == ButtonTile.UNCOVERED:
                    uncovered += 1

            # end for col
        # end for row

        # the second compare may be all that is needed
        # if (invalid_flagged == 0 and valid_flagged == self._number_of_mines) and \
        if (uncovered + self._valid_flagged) == (self._size**2):
            ret = True
        # end if

        return ret
    # end is_game_over


    def set_tile(self, row: int, col: int ,value: int) -> None:
        self._field_grid[make_name(row,col)].set_value(value)
    # end set_tile


    def get_tile(self,row: int, col: int):
        return self._field_grid[make_name(row, col)]
    # end get_tile

# module function
def make_name(row: int, col: int) -> str:
    return str(row) + ',' + str(col)
# end

