"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: Linda Spellman

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  
  
- Display the numbers received by the reader printing them to the console.

- Create WRITERS writer processes

- Create READERS reader processes

- You can use sleep() statements for any process.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s), or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

- When each reader reads a value from the sharedList, use the following code to display
  the value:
  
                    print(<variable>, end=', ', flush=True)

Add any comments for me:


"""
import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp
import threading 

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2


def write(semaphore, lock, shared_list):
    for i in shared_list:
        i.write()

def read(semaphore, lock, shared_list, count):
    for i in shared_list:
        i.read()
        count += 1
        print(i, end=', ', flush=True)
    return count 

def main():
    # Can treat this like Factory and Dealer - 2 semaphores and 1 lock for the buffer - implementing your own "queue" with size 10 - buffering memory

    # This is the number of values that the writer will send to the reader
    items_to_send = random.randint(1000, 10000)

    smm = SharedMemoryManager()
    smm.start()

    # TODO - Create a ShareableList to be used between the processes
    shared_list = smm.ShareableList(range(BUFFER_SIZE))

    # TODO - Create any lock(s) or semaphore(s) that you feel you need
    been_read = threading.Semaphore(BUFFER_SIZE)
    been_written = threading.Semaphore(0) 

    buffer_lock = threading.Lock() 

    # TODO - create reader and writer processes - 2 of each
    writers = []
    writer1 = mp.Process(target=write, args=(been_written, buffer_lock, shared_list, ))
    writers.append(writer1)
    writer2 = mp.Process(target=write, args=(been_written, buffer_lock, shared_list, )) 
    writers.append(writer2)

    readers = []
    read_count = 0
    reader1 = mp.Process(target=read, args=(been_read, buffer_lock, read_count, ))
    readers.append(reader1)
    reader2 = mp.Process(target=read, args=(been_read, buffer_lock, read_count, ))
    readers.append(reader2)

    # TODO - Start the processes and wait for them to finish
    for i in writers:
        i.start()

    for i in readers:
        i.start()

    for i in writers:
        i.join()

    for i in readers:
        i.join() 

    print(f'{items_to_send} values sent')

    # TODO - Display the number of numbers/items received by the reader.
    #        Can not use "items_to_send", must be a value collected
    #        by the reader processes.
    # print(f'{<your variable>} values received')

    smm.shutdown()


if __name__ == '__main__':
    main()
