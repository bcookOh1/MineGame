from tkinter.simpledialog import Dialog, askstring
from tkinter import Tk, Frame, Label, constants
from scoreFileIO import ScoreFileIO

class TopScoresDlg(Dialog):

    def __init__(self, parent, latest):

        self._parent = parent
        self._latest_score = latest

        # self.parent.bind("<Return>", lambda x: print("You pressed enter"))

        Dialog.__init__(self, parent, 'Top Scores')

    # end init

    # override from base dialog class
    def body(self, parent):

        self._score_file_io = ScoreFileIO('topscores.json')
        self._score_file_io.read_in_scores()

        self._frame = Frame(self, pady=10, padx=10)

        # start filling the dialog
        congrats_lbl = Label(self._frame, text="Top Scores")
        congrats_lbl.config(pady=10, padx=10, fg="blue", font=("arial", 14, "bold"))
        congrats_lbl.grid(row=0, column=0, columnspan=5)

        # start of the row column grid for (tabular) scores
        col0_lbl = Label(self._frame, text="place", width=4, font=("arial", 12, "normal"))
        col0_lbl.grid(row=1, column=0)
        col1_lbl = Label(self._frame, text="score", width=6, font=("arial", 12, "normal"))
        col1_lbl.grid(row=1, column=1)
        col2_lbl = Label(self._frame, text="name", width=16, font=("arial", 12, "normal"))
        col2_lbl.grid(row=1, column=2)
        col3_lbl = Label(self._frame, text="date", width=10, font=("arial", 12, "normal"))
        col3_lbl.grid(row=1, column=3)
        self._frame.pack(side=constants.TOP)

        # if latest score is a leader then ask for a name else just display
        # top scores
        if self._score_file_io.is_leader(self._latest_score) == True:
            self._parent.after(100, self.get_leader_name)
        else:
            self.show_scores(-1)

    # end body

    def apply(self):
        return 'break'
    # end apply


    def show_scores(self, new_index: int):

        score_list = self._score_file_io.get_score_list()

        for idx in range(len(score_list)):

            # used for the grid row index which alrready contains text
            # and column headers
            row_index = idx + 2

            # highlight the newly score row
            if new_index == idx:
                row_color: str = "cyan1"
            else:
                row_color: str = "light gray"

            # in each label use .configure() for additional items
            number_place_lbl = Label(self._frame, text=str(idx + 1) + ")", bg=row_color)
            number_place_lbl.configure(width=4, font=("arial", 12, "normal"))
            number_place_lbl.grid(row=row_index, column=0, sticky=constants.E+constants.W)

            latest_score_lbl = Label(self._frame, text=str(score_list[idx][ScoreFileIO.SCORE_KEY]), bg=row_color)
            latest_score_lbl.configure(width=6, font=("arial", 12, "normal"))
            latest_score_lbl.grid(row=row_index, column=1, sticky=constants.E+constants.W)

            first_name_lbl = Label(self._frame, text=score_list[idx][ScoreFileIO.NAME_KEY], bg=row_color )
            first_name_lbl.configure(width=16, font=("arial", 12, "normal"))
            first_name_lbl.grid(row=row_index, column=2, pady=5, sticky=constants.E+constants.W)

            date_lbl = Label(self._frame, text=score_list[idx][ScoreFileIO.DATE_KEY], bg=row_color)
            date_lbl.configure(width=10, font=("arial", 12, "normal"))
            date_lbl.grid(row=row_index, column=3, sticky=constants.E+constants.W)

        else:
            self._frame.pack(side=constants.TOP)

    # end show_score


    def get_leader_name(self) -> None:

        title_str: str = "New Top Score, " + str(self._latest_score)
        new_top_score_name = askstring(title_str, "Enter your name (15char max):", parent=self._parent)

        if new_top_score_name == None:
           new_top_score_name = "mr. no-name"
        # end if

        new_index: int = self._score_file_io.add_new_score( self._latest_score, new_top_score_name)
        self._score_file_io.save_scores()
        self.show_scores(new_index)

    # end get_leader_name

    '''
    def apply(self):
    end apply
    '''

if __name__ == "__main__":

    scores = [
        {"score": 100, "name": "Tommy", "date": "03-06-2021"},
        {"score": 200, "name": "a winner", "date": "03-07-2021"},
        {"score": 300, "name": "Pips", "date": "03-08-2021"},
        {"score": 400, "name": "Manny", "date": "03-09-2021"}
    ]

    root = Tk()
    latest_score: int = 250
    s = TopScoresDlg(root, latest_score)
    # print(s['highScore'])
    root.mainloop()
