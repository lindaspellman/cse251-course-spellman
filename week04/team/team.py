"""
Course: CSE 251
Lesson Week: 04
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- See in I-Learn

"""

import threading
import queue
import requests
import json

# Include cse 251 common Python files
from cse251 import *

RETRIEVE_THREADS = 4        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

def retrieve_thread(que, log):  # TODO add arguments
    """ Process values from the data_queue """

    while True:
        # TODO check to see if anything is in the queue
        url = que.get() # block if empty

        # TODO process the value retrieved from the queue
        url = que.get()
        if url == NO_MORE_VALUES:
            return

        print(url)
        
        # # TODO make Internet call to get characters name and log it
        # response = requests.get(url)
        #     # Check the status code to see if the request succeeded.
        # if response.status_code == 200:
        #     data = response.json()
        # else:
        #     print('Error in requesting. Response = ', response.status_code)

        # log.write(data.get("name"))


def file_reader(filename, que, log): # TODO add arguments
    """ This thread reading the data file and places the values in the data_queue """

    # TODO Open the data file "urls.txt" and place items into a queue
    with open(filename) as file:
        for line in file:
            url = line.trip()
            queue.put(url)
    
    log.write('finished reading file')

    # TODO "signal" the retrieve threads one more time that there are "no more values"
    for i in range(RETRIEVE_THREADS):
        que.put(NO_MORE_VALUES)


def main():
    """ Main function """

    log = Log(show_terminal=True)

    # TODO create queue
    que = queue.Queue()

    # TODO create semaphore (if needed)
    # workers = threading.Semaphore(RETRIEVE_THREADS)

    # workers.acquire()
    # # Do something
    # workers.release()

    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread need to do their job
    reader = threading.Thread(target=file_reader, args=('urls.txt', que, log)) 
    
    workers = []
    for i in range(RETRIEVE_THREADS):
        worker = threading.Thread(target=retrieve_thread, args=(que, log))
        worker.append(worker)

    log.start_timer()

    # TODO Get them going - start the retrieve_threads first, then file_reader
    reader.start() # non-blocking
    worker.start()

    # TODO Wait for them to finish - The order doesn't matter
    reader.join()
    worker.join()

    log.stop_timer('Time to process all URLS')


if __name__ == '__main__':
    main()




