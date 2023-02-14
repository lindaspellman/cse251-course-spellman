"""
Author: Bro. Comeau

- Create a program to have a boss-worker architecture.
- The Purpose of the program is to fill in cells in a shared matrix (N x N)
- create a thread to add commands to a pipe 
"""
import time
import random
import multiprocessing as mp

N = 100
WORKERS = 5
COMMANDS = 10

def boss_func(pipes):
    for i in range(COMMANDS):
        x = random.randint(0, N - 1)
        y = random.randint(0, N - 1)
        pipes[i % WORKERS][0].send((x,y))
    
    # all done
    for i in range(WORKERS):
        pipes[i][0].send(-1)

    # pass 

def worker_func(connection, index, mat, locks):
    while True:
        item = connection.recv()
        if item == -1:
            break

        # print(item)
        x, y = item 
        with locks[y * N + x]:
            mat[y * N + x] += 1

    # pass

def main():
    # mat
    mat = mp.Manager().list([0] * N ** 2) # one list

    locks = []
    for i in range(N ** 2):
        locks.append(mp.Lock())

    # create pipes
    pipes = []
    for i in range(WORKERS):
        parent, child = mp.Pipe()
        pipes.append((parent,child))

    # create boss and workers
    boss = mp.Process(target=boss_func, args=(pipes,))
    workers = []
    for i in range(WORKERS):
        worker = mp.Process(target=worker_func, args=(pipes[i][1], i, mat, locks,))

    # start
    boss.start()
    for w in workers:
        w.start()

    # join
    boss.join()
    for w in workers:
        w.join()

    # display results
    print(mat)
    print(sum(mat))


if __name__ == "__main__":
    main()