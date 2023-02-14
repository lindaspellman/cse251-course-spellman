"""
Course: CSE 251
Lesson Week: 05
File: team.py
Author: Brother Comeau

Purpose: Check for prime values

Instructions:

- You can't use thread pools or process pools
- Follow the graph in I-Learn 
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it

"""
import time
import threading
import multiprocessing as mp
import random
from os.path import exists



#Include cse 251 common Python files
from cse251 import *

PRIME_PROCESS_COUNT = 5

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# TODO create read_thread function
def reader_thread(filename, shared_que):
    with open(filename, 'r') as file:
        for line in file:
            shared_que.put(int(line))
    # all done message
    for i in range(PRIME_PROCESS_COUNT):
        shared_que.put(-1)

# TODO create prime_process function
def process_prime(que, primes):
    while True: 
        number = que.get()
        if number < 0:
            break 
        if is_prime(number):
            primes.append(number)
    
    # finish up
    return 

def create_data_txt(filename):
    # only create if is doesn't exist 
    if not exists(filename):
        with open(filename, 'w') as f:
            for _ in range(1000):
                f.write(str(random.randint(10000000000, 100000000000000)) + '\n')


def main():
    """ Main function """

    filename = 'data.txt'
    create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create shared data structures
    shared_que = mp.Manager().Queue()
    primes = mp.Manager().list()

    # TODO create reading thread
    reader = threading.Thread(target=reader_thread, args=(filename, shared_que))

    # TODO create prime processes
    processes = [ mp.Process(target=process_prime, args=(shared_que, primes)) for i in range(PRIME_PROCESS_COUNT)]

    # TODO Start them all
    for p in processes:
        p.start()
    reader.start()

    # TODO wait for them to complete
    reader.join()
    for p in processes:
        p.join()

    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)


if __name__ == '__main__':
    main()

