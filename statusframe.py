from tkinter import *

class StatusFrame(Frame):

    # consts values for face button
    HAPPY_FACE: int = 0
    UH_HO_FACE: int = 1
    WIN_FACE: int = 2

    def __init__(self, top, mcount: int=0, tim: int =0, face_num: int =0):
        Frame.__init__(self, top, bd=1, relief=FLAT)
        self._mine_count = mcount
        self._game_time = tim
        self._face_number = face_num

        self._win_face = PhotoImage(file='./gifs/winner.gif')
        self._hap_face = PhotoImage(file='./gifs/happy_face.gif')
        self._uh_oh_face = PhotoImage(file='./gifs/uh-oh_face.gif')

        self._mine_counter_lbl = Label(self, width=5, text=str(self._mine_count))
        self._mine_counter_lbl.config(fg="blue", font=("arial", 12, "bold"))

        self._new_button = Button(self, padx=20, name='faceButton', image=self._hap_face)
        # self._new_button.bind("<Button-1>", self.on_new_button_clicked)

        self._game_timer_lbl = Label(self, width=5, text=str(self._game_time))
        self._game_timer_lbl.config(fg="blue", font=("arial", 12, "bold"))

        self._mine_counter_lbl.grid(row=0, column=0)
        self._new_button.grid(row=0, column=1)
        self._game_timer_lbl.grid(row=0, column=2)
    # end __init__

    """
    def on_new_button_clicked(self, event):
        print("before event_generate")
        self.event_generate("<<New_Game_Clicked>>", when="tail") # when="tail" acts like WIN post message
        print("after event_generate")
    # end on_new_button_clicked
    """

    def set_mine_counter(self, val: int) -> None:
        self._mine_count = val
        self._mine_counter_lbl.config(text=str(self._mine_count))
    # end set_mine_counter


    def set_game_timer(self, val: int) -> None:
        self._game_time = val
        self._game_timer_lbl.config(text=str(self._game_time))
    # end set_game_timer


    def set_button_face(self, face_num: int) -> None:
        self._face_number = face_num
        if self._face_number == StatusFrame.UH_HO_FACE:
            self._new_button.config(image=self._uh_oh_face)
        elif self._face_number == StatusFrame.WIN_FACE:
            self._new_button.config(image=self._win_face)
        else:
            self._new_button.config(image=self._hap_face)
        # end if

    # end set_button_face

if __name__ == "__main__":
    root = Tk()
    s = StatusFrame(root,123,432,0)
    s.pack()
    # s.bind("<<New_Game_Clicked>>", lambda x: print("<<New_Game_Clicked>> event") )
    s.mainloop()

