Author: Andrew Frantzich

This remake of minesweeper was done with python 2.7

To convert to python 3, I believe all you need to do is remove the first line (from __future__ ...) and 
change raw_input on lines 168, 170, and 203 to input, though I may have overlooked something.

Running the program can either take 0, 1, or 3 parameters

Running without parameters automatically starts the game in expert mode

Using 1 parameter, you can use 'expert/hard', 'intermediate/medium/normal', or 'easy/beginner' to set difficulty

Using 3 parameters creates a custom map of width, height, and number of bombs.

Neither invalid parameters nor maximum recursion depth have been handled. :(

The height variable uses ascii values from 65 upward. Suggested max height is 26, but up to 32 can be handled.
The 'a' character for row 33 cannot be handled since the program sets input to uppercase.

Enjoy!
