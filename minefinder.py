import re
from tkinter import Tk
from statusframe import StatusFrame
from fieldframe import FieldFrame
from buttontile import ButtonTile
from topscores import TopScores


class MineFinder:

    _MAX_TIME: int = 6000
    _LENGTH_OF_SIDE: int = 15
    _PERCENT_MINES: float = 15.0

    def __init__(self):
        self._size: int = MineFinder._LENGTH_OF_SIDE
        self._root = Tk()
        self._game_active: bool = False
        self._game_time: int = 0
        self._game_over: bool = False
        self._timer_id = None
        self._root.title('Mine Finder')
        self._status_frame = StatusFrame(self._root ,0 ,0 ,0)
        self._field_frame = FieldFrame(self._root, self._size, MineFinder._PERCENT_MINES)
        self._timer_id = self._root.after(1000, self.game_timer)
    # end __init__


    def __del__(self):
        self._root.after_cancel(self._timer_id)
    # end __del__


    def display_gui(self):
        self.set_status_frame()
        self.set_field_frame()

        self._field_frame.print_contents()
        self._root.mainloop()
    # end display_gui


    def set_status_frame(self):
        self._status_frame.grid(row=0, column=0)
        self._status_frame.bind_class('Button','<ButtonRelease-1>', self.new_game_clicked,'+')
    # endset_status_frame


    def set_field_frame(self):
        self._field_frame.field_grid_to_gui()
        self._field_frame.bind_class('Button', '<ButtonRelease-1>', self.frame_left_mouse,'+')
        self._field_frame.bind_class('Button', '<ButtonRelease-3>', self.frame_right_mouse)
        self._field_frame.grid(row=1, column=0)
    # end set_field_frame


    def layout_mines(self):

        self.game_time = 0
        self._field_frame.init_field_grid()
        self._field_frame.place_mines()
        self._field_frame.set_adjacent()
        self._status_frame.set_mine_counter(self._field_frame.undiscoverd_mines())
        self._status_frame.set_game_timer(self._game_time)

    # end set_field_frame


    def new_game_clicked(self, event):

        if str(event.widget) == '.!statusframe.faceButton':
            self.layout_mines()
            self._status_frame.set_button_face(StatusFrame.HAPPY_FACE)
            self._game_active = False
            self._game_over = False
            self._game_time = 0

             # prevents propagation when callback is in top but event
             # is from widget in child frame
            return 'break'

        # end if
    # end new_game_clicked


    def frame_left_mouse(self, event):

        # ignore if the game is over
        if self._game_over == False:

            # look for specific widget names
            result = re.match('^.!fieldframe.!buttontile[0-9]{0,4}$', str(event.widget))
            if result != None:

                # ignore if cover is flag, question, or blank
                if event.widget._cover == ButtonTile.COVER_BLANK:

                    if self._game_active == False:
                        self._game_active = True

                    event.widget.uncover()

                    if event.widget.get_value() == 0:
                        r,c = event.widget.get_row_col()
                        self._field_frame.show_clear_tiles(r, c)
                    # end if

                    # game is over if mine is uncovered
                    if event.widget.get_value() == FieldFrame.MINE_VALUE:
                        self._game_active = False
                        self._game_over = True
                        self._status_frame.set_button_face(StatusFrame.UH_HO_FACE)
                        self.show_top_score_dialog()

                    # check if game is over when all mines are flagged
                    elif self._field_frame.is_game_over() == True:
                        self._game_active = False
                        self._game_over = True
                        self._status_frame.set_button_face(StatusFrame.WIN_FACE)
                        self.show_top_score_dialog(True)
                    # end if

                    # must follow  is_game_over()
                    self._status_frame.set_mine_counter(self._field_frame.undiscoverd_mines())

                    # self._field_frame.print_contents()

                    # prevents propagation when callback is in top but
                    # event is from widget in child frame
                    return 'break'
                # end if
            # end if

        # end if

    # end frame_left_mouse


    def frame_right_mouse(self, event):

        # ignore if the game is over
        if self._game_over == False:

            # look for specific widget names
            result = re.match('^.!fieldframe.!buttontile[0-9]{0,4}$', str(event.widget))
            if result != None:

                # ignore if cover is uncovered
                if event.widget._cover != ButtonTile.UNCOVERED:

                    if self._game_active == False:
                        self._game_active = True

                    event.widget.set_cover()

                    if self._field_frame.is_game_over() == True:
                        self._game_active = False
                        self._game_over = True
                        self._status_frame.set_button_face(StatusFrame.WIN_FACE)
                        self.show_top_score_dialog(True)
                    # end if

                    # must follow  is_game_over()
                    self._status_frame.set_mine_counter(self._field_frame.undiscoverd_mines())

                    # self._field_frame.print_contents()

                    # prevents propagation when callback is in top but
                    # event is from widget in child frame
                    return 'break'
                # end if
            # end if

    # end frame_right_mouse


    def game_timer(self):

        if self._game_active == True:
            self._game_time += 1
            self._status_frame.set_game_timer(self._game_time)

            # if timeout of 10min then game lost
            if self._game_time >= MineFinder.MAX_TIME:
                self._game_active = False
                self._game_over = True
                self._status_frame.set_button_face(StatusFrame.UH_HO_FACE)
                self.show_top_score_dialog()
            # end if

        # end if

        self._status_frame.set_game_timer(self._game_time)
        self._timer_id = self._root.after(1000, self.game_timer)

    # end game_timer


    # just need to instatiate HighScoresDlg()
    def show_top_score_dialog(self, test_for_win: bool=False) -> None:

        # use conditional to pass self._game_time
        # else MineGame.MAX_TIME as non-win
        time: int = self._game_time if test_for_win else MineFinder.MAX_TIME
        TopScores(self._root, time)

    # end show_top_score_dialog


if __name__ == "__main__":
    m = MineFinder()
    m.layout_mines()
    m.display_gui()
