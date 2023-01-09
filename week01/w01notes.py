"""
Course: CSE251
Lesson Week: 01
File: lesson.py
Author: Brother Comeau
"""

import time

# TODO Create a Python class
class Person:

    def __init__():
        pass

    def run(self):
        pass


def inner_functions():
    """ Example of using an inner function """

    x = 9

    def display_hello():
        nonlocal x
        x += 10
        print('Hello', x)

    display_hello()


def display_hello1():
    print('Hello 111111111')


def display_hello2():
    print('Hello 222222222')


def display_hello3():
    print('Hello 333333333')


def functions():

    # this is a list of pointers to functions 
    functions = [
        display_hello1,
        display_hello2,
        display_hello3,
    ]

    # call each function
    for function in functions:
        function()


def pass_by_value(x):
    # x: int, float, string, bool
    pass


def pass_by_reference(x):
    # lists, dict, sets, objects
    pass


def variables():
    # Using globals variables (global)
    # pass by value -VS- pass by reference
    pass


def data_structures():
    # list
    # - list of numbers (create, add, remove, loop)
    # - [0] * N example
    # - list comprehension
    # - in operator

    # Tuple
    # - one item in a tuple

    # dictionary
    # - creating, adding, in operator
    pass


def files():
    # read and write files (VSCode issue)
    pass


def recursion(x):
    # Functions calling themselves
    print(x)
    recursion(x + 1)


def main():
    functions()
    variables()
    inner_functions()
    data_structures()
    files()
    # recursion(0)


if __name__ == '__main__':
    main()
