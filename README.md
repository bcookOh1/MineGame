**Mine Sweeper Game**

This game repoduces one that came with older versions of Microsoft Windows. The game is not completely fathful to the original, but is very playable. It's written in python and uses tkinter for the GUI. I wrote this as a way to learn some python and tkinker programming and best practices.

**How to play:**
1. the game starts with all tiles covered
   1. left click on a tile to uncover it and that tile can be blank, a number [1..8], or a bomb
      1. if blank the game will uncover any adjacent blank or numbered tiles recursively,
         1. if the tile is a number then only that tile is uncovered
      1. if a bomb then game over
   1. right click on a tile to tag it with a flag or question mark
      1. continuing to right click will cycle through the above
      1. you can only left click on untagged tile
1. the game is over you uncover a bomb (lose), or flag each bomb and uncover all other tiles (win)
1. the time is kept while you play
1. at the end of a game the program shows you the top scores dialog,
   if your time is among the top (low) scores the program asks for a name and adds it to the top scores.
