"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p1.py 
Author: Linda Spellman

Purpose: Part 1 of assignment 09, finding a path to the end position in a maze

Instructions:
- Do not create classes for this assignment, just functions.
- Do not use any other Python modules other than the ones included.

"""
import math
from screen import Screen
from maze import Maze
import cv2
import sys

# Include cse 251 files
from cse251 import *

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
SLOW_SPEED = 100
FAST_SPEED = 1
speed = SLOW_SPEED

# TODO add any functions

def solve_path(maze):
    """ Solve the maze and return the path found between the start and end positions.  
        The path is a list of positions, (x, y) """
        
    # TODO start to add code here
    path = []
    start_x, start_y = maze.get_start_pos()
    maze.move(start_x, start_y, COLOR)
    path.append((start_x, start_y))

    def _solve(x, y):
        possible_moves = maze.get_possible_moves(x, y)
        # if possible_moves's [] returns nothing: it's the end I guess???
        if possible_moves == []:
            return False
        for (x,y) in possible_moves:
            if maze.at_end(x, y):
                maze.move(x, y, COLOR)
                path.append((x, y))
                return True 
            # if maze.can_move_here(x, y):
            maze.move(x, y, COLOR)
            path.append((x, y))
            if _solve(x,y):
                return True
                # start_pos becomes a possible new move. How to say "don't go back"?
            # if new_move == maze.at_end(move[0], move[1]):
            #     path.append(move)
            maze.restore(x, y)
            path.pop() 
        
        return False 
                
    _solve(start_x, start_y)

    return path 



def get_path(log, filename):
    """ Do not change this function """
    #  'Maze: Press "q" to quit, "1" slow drawing, "2" faster drawing, "p" to play again'
    global speed

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename)

    path = solve_path(maze)

    log.write(f'Number of drawing commands for = {screen.get_command_count()}')

    done = False
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('1'):
                speed = SLOW_SPEED
            elif key == ord('2'):
                speed = FAST_SPEED
            elif key == ord('q'):
                exit()
            elif key != ord('p'):
                done = True
        else:
            done = True

    return path


def find_paths(log):
    """ Do not change this function """

    files = ('verysmall.bmp', 'verysmall-loops.bmp', 
            'small.bmp', 'small-loops.bmp', 
            'small-odd.bmp', 'small-open.bmp', 'large.bmp', 'large-loops.bmp')

    log.write('*' * 40)
    log.write('Part 1')
    for filename in files:
        log.write()
        log.write(f'File: {filename}')
        path = get_path(log, filename)
        log.write(f'Found path has length          = {len(path)}')
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_paths(log)


if __name__ == "__main__":
    main()