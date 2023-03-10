"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p2.py 
Author: Linda Spellman

Purpose: Part 2 of assignment 09, finding the end position in the maze

Instructions:
- Do not create classes for this assignment, just functions.
- Do not use any other Python modules other than the ones included.
- Each thread requires a different color by calling get_color().


This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the exit position.

What would be your strategy?  

<Answer here>

Why would it work?

<Answer here>

"""
import math
import threading 
from screen import Screen
from maze import Maze
import sys
import cv2

# Include cse 251 files
from cse251 import *

SCREEN_SIZE = 700
COLOR = (0, 0, 255)
COLORS = (
    (0,0,255),
    (0,255,0),
    (255,0,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128),
    (72,61,139),
    (143,143,188),
    (226,138,43),
    (128,114,250)
)
SLOW_SPEED = 100
FAST_SPEED = 0

# Globals
current_color_index = 0
thread_count = 0
stop = False
speed = SLOW_SPEED

def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color

def _solve(maze, x, y, lock, thread_color):
    # nonlocal path = [] 
    global stop 
    global thread_count 
    # thread_color = COLOR # how to not declare it???
    # can you put the lock inside maze.move(...)?
    # ask Michael and teacher
    # global lock?
    # how to set the color once for each thread? 
    # Thread local storage variable, static function?
    # nonlocal vs global variables? 
    if stop == True:
        return
    
    # race condition
    with lock: 
        if maze.can_move_here(x, y):
            maze.move(x, y, thread_color)
        else:
            return
    
    with lock:
        possible_moves = maze.get_possible_moves(x, y)

    if possible_moves == []:
        return
    
    main_x, main_y = possible_moves.pop()

    threads = []
    for (x,y) in possible_moves:
        new_thread_color = get_color() 
        # spawn new thread before testing for end
        with lock:
            if maze.can_move_here(x,y):
                new_thread = threading.Thread(target=_solve, args=(maze, x, y, lock, new_thread_color))
                threads.append(new_thread)
                thread_count += 1
        # new_thread.thread_color = get_color() # feasible?
    

    for t in threads:
        t.start() 

    # with lock: 
    if maze.at_end(x,y):
        maze.move(x, y, thread_color)
        stop = True 
        
    else:
        # x, y = possible_moves[0]
        # _solve(maze, x, y)
        _solve(maze, main_x, main_y, lock, thread_color)
        
    # _solve(maze, main_x, main_y, lock, thread_color) 

    if stop == True:
        return

    for t in threads:
        t.join()
    
    # if stop == True:
    #     return
    
    # return stop 
    # pass

def solve_find_end(maze):
    """ finds the end position using threads.  Nothing is returned """
    # When one of the threads finds the end position, stop all of them
    global stop 
    stop = False 
    lock = threading.Lock()
    color = get_color() 

    start_x, start_y = maze.get_start_pos()
    _solve(maze, start_x, start_y, lock, color)

    # ### INNER FUNCTION HERE!!!!!!!!!!!!!!!???????????????
    # # breadth-first search is not recursive, depth-first algorithm is
    # def _solving_maze(x, y, thread_color):
    #     # nonlocal path = [] 
    #     global stop 
    #     # thread_color = COLOR # how to not declare it???
    #     # can you put the lock inside maze.move(...)?
    #     # ask Michael and teacher
    #     # global lock?
    #     # how to set the color once for each thread? 
    #     # Thread local storage variable, static function?
    #     # nonlocal vs global variables? 

    #     if stop == True:
    #         return 
        
    #     # race condition
    #     if maze.can_move_here(x, y):
    #         maze.move(x, y, thread_color)
    #     else:
    #         return 
        
    #     possible_moves = maze.get_possible_moves(x, y)

    #     if possible_moves == []:
    #         return

    #     threads = []
    #     for (x,y) in possible_moves[1:]:
    #         # spawn new thread before testing for end
    #         new_thread = threading.Thread(target=_solving_maze, args=(x, y, thread_color))
    #         # threads.append(new_thread)
    #         # new_thread.thread_color = get_color() # feasible?
    #         new_thread.start()

    #     if maze.at_end(x,y):
    #         maze.move(x, y, thread_color)
    #         stop = True 
    #     else:
    #         x, y = possible_moves[0]
    #         _solving_maze(x, y, thread_color)

    #     for t in threads:
    #         t.join()
        
    #     return

    # _solving_maze(start_x, start_y, get_color())


def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count
    global speed

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

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



def find_ends(log):
    """ Do not change this function """

    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)



if __name__ == "__main__":
    main()