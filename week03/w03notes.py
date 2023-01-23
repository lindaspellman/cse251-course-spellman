import time 
import os
import multiprocessing as mp

def func(name):
    time.sleep(0.5)
    print(f'{name}, {os.getpid()}')

if __name__ == '__main__':
    names = ['John','Mary','Linda']

    # USE POOL FOR ASGMT
    with mp.Pool(3) as p: # Pool creates 3 mp processes
        p.map(func, names) # blocking call!!!