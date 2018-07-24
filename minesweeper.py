# minesweeper.py
# establish a variable board based on 3 int input. row, col, #ofbombs
# by afrantzi

from __future__ import print_function
import os
import sys
import random

row = 0
col = 0
nbombs = 0
win = 0
marked = 0
game_over = 0
cheat = 0
input_mode = "show"
save = {}

def add_heat(bombs, x, y):
    global row, col
    if y > 0:
        if bombs[x][y - 1] != '*': bombs[x][y - 1] += 1
    if y < col - 1:
        if bombs[x][y + 1] != '*': bombs[x][y + 1] += 1
    if x > 0:
        if bombs[x - 1][y] != '*': bombs[x - 1][y] += 1
        if y > 0:    
            if bombs[x - 1][y - 1] != '*': bombs[x - 1][y - 1] += 1
        if y < col - 1:
            if bombs[x - 1][y+ 1] != '*': bombs[x - 1][y + 1] += 1
    if x < row - 1: 
        if bombs[x + 1][y] != '*': bombs[x + 1][y] += 1
        if y > 0:
            if bombs[x + 1][y - 1] != '*': bombs[x + 1][y - 1] += 1
        if y < col - 1:
            if bombs[x + 1][y + 1] != '*': bombs[x + 1][y + 1] += 1

def randomize_bombs():
    global row, col, nbombs
    bombs = [[0 for j in range(col)] for i in range(row)]
    cbomb = 0
    while cbomb < nbombs:
        x = random.randrange(0, row)
        y = random.randrange(0, col)
        if bombs[x][y] != '*':
            bombs[x][y] = '*'
            add_heat(bombs, x, y)
            cbomb += 1
    return bombs

def print_row(row_name, myrow, checked):
    global col
    for i in range(col):
        if i == 0:
            print('  ', end='')
        print (' ---', end='')
    print('')
    for i in range(col):
        display = myrow[i]
        if display == 0: display = ' '
        if checked[ord(row_name) - 65][i] == 0:
            display = '\x1b[0;30;47m \x1b[0m'
        elif checked[ord(row_name) - 65][i] == 2:
            display = '\x1b[0;30;47mX\x1b[0m'
        elif checked[ord(row_name) - 65][i] == 3:
            display = '\x1b[0;31;47mO\x1b[0m'
        if i == 0:
            print(row_name, '', end='')
        print('|', display, '', end='')
    print('|',  row_name)

def print_board(bombs, checked):
    global row, col
    print('                                  -----------------------------------------------------')
    print('        bombs left: ', nbombs - marked, '                          M I N E S W E E P E R                 ')
    print('                                  -----------------------------------------------------\n')
    for i in range(col):
        if i == 0:
            print(' ', end='')
        print('  {0:2d}'.format(i) , end='')
    print('')
    for i in range(int(row)):
        print_row(chr(i + 65), bombs[i], checked)
    for i in range(int(col)):
        if i == 0:
            print('  ', end='')
        print(' ---', end='')
    print('')
    for i in range(col):
        if i == 0:
            print(' ', end='')
        print('  {0:2d}'.format(i) , end='')
    print('')

def check_error(s):
    global row, col
    if len(s) < 2 or len(s) > 3:
        return (1)
    for i in s[1:]:
        if i < '0' or i > '9':
            return (1)
    else:
        r = int(s[1:])
    if s[0] >= 'A' and s[0] <= chr(ord('A') + (row - 1)):
        if r >= 0 and r <= col: return 0
    return (1)

def print_all(bombs):
    global row, col
    print('')
    for i in range(row):
        for j in range(col):
            print(bombs[i][j], ' ', end='')
        print('')

def spread(bombs, checked, x, y):
    global row, col
    if y > 0: check_location(bombs, checked, x, y - 1)
    if y < col - 1: check_location(bombs, checked, x, y + 1)
    if x > 0:
        check_location(bombs, checked, x - 1, y)
        if y > 0: check_location(bombs, checked, x - 1, y - 1)
        if y < col - 1: check_location(bombs, checked, x - 1, y + 1)
    if x < row - 1:
        check_location(bombs, checked, x + 1, y)
        if y > 0: check_location(bombs, checked, x + 1, y - 1)
        if y < col - 1: check_location(bombs, checked, x + 1, y + 1)

def check_location(bombs, checked, x, y):
    global game_over, input_mode, row, col, marked, win
    if checked[x][y] == 0:
        if input_mode == 'show':
            checked[x][y] = 1
            if bombs[x][y] == '*':
                game_over = 1
            elif bombs[x][y] == 0:
                spread(bombs, checked, x, y)
            win -= 1
            if win == 0 and game_over == 0:
                game_over = 2
        elif input_mode == 'mark':
            checked[x][y] = 2
            marked += 1
    elif checked[x][y] == 2 and input_mode == 'mark':
        checked[x][y] = 0
        marked -= 1

def reveal(bombs, checked):
    global row, col, game_over
    for i in range(row):
        for j in range(col):
            if game_over == 1:
                if bombs[i][j] == '*' and checked[i][j] != 2: checked[i][j] = 1
                elif bombs[i][j] != '*' and checked[i][j] == 2: checked[i][j] = 3
            if game_over == 2:
                if bombs[i][j] == '*' and checked[i][j] != 1: checked[i][j] = 2

def end_q(bombs, checked):
    global game_over, save, row, col
    os.system('clear')
    reveal(bombs, checked)
    print_board(bombs, checked)
    if game_over == 2:
        print("\nyippy skippy!\n you won!")
    else:
        print("\ngame over")
    redo = raw_input("play again? (y/n): ")
    if redo.lower() == 'y':
        redo = raw_input("same map? (y/n): ")
        if redo.lower() == 'y':
            game_over = 0
            checked = [[0 for j in range(col)] for i in range(row)]
            turn(bombs, checked)
        elif redo.lower() == 'n':
            game_over = 0
            main(save)
    elif redo.lower() == 'n': exit()
    end_q(bombs, checked)
            
def command(bombs, checked, s):
    global row, col, cheat, input_mode
    if s.lower() == 'cheat': 
        if cheat == 0: cheat = 1
        else: cheat = 0
    elif s.lower() == 'mark' or s.lower() == 'show':
        input_mode = s.lower()
    elif s.lower() == 'quit' or s.lower() == 'exit' or s.lower() == ':q':
        exit()
    elif check_error(s.upper()) == 0:
        check_location(bombs, checked, ord(s[0].upper()) - 65, int(s[1:]))

def turn(bombs, checked):
    global game_over, input_mode, cheat, row, col
    while (game_over == 0):
        os.system('clear')
        print_board(bombs, checked)
        if cheat == 1:
            print('')
            print_all(bombs)
        print("\nType 'mark/show' to change modes.")
        prompt = input_mode + " location(A1, c12, etc.): "
        s = raw_input(prompt)
        command(bombs, checked, s)
    end_q(bombs, checked)

def set_all(length, height, num_bombs):
    global row, col, nbombs, win
    col = length
    row = height
    nbombs = num_bombs
    win = row * col - nbombs

def main(argv):
    global save, row, col, nbombs
    save = argv
    if len(argv) == 1 or argv[1] == 'expert' or argv[1] == 'hard':
        set_all(30, 16, 99)
    elif argv[1] == 'normal' or argv[1] == 'medium' or argv[1] == 'intermediate':
        set_all(16, 16, 40)
    elif argv[1] == 'beginner' or argv[1] == 'easy':
        set_all(9, 9, 10)
    elif len(argv) == 3:
        set_all(int(argv[1]), int(argv[2]), int(argv[1]) * int(argv[2]) / 6)
    else:
        set_all(int(argv[1]), int(argv[2]), int(argv[3]))
    bombs = randomize_bombs()
    checked = [[0 for j in range(col)] for i in range(row)]
    turn(bombs, checked)

main(sys.argv)
