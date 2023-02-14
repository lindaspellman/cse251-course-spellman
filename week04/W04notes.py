# learn list comprehension
# just one line of code, super fast

# a Semaphore of 1 is a Lock

# QUEUES - thread-safe data structure
# put() to enqueue
# get() to dequeue

# import queue

# q = queue.Queue()

# q.put('House')
# q.put('tree')
# q.put('Farm')
# q.put('Truck')

# print(f'Size of queue = {q.qsize()}')
# print(f'Get an item from the queue: {q.get()}')

# print(f'Size of queue = {q.qsize()}')
# print(f'Get an item from the queue: {q.get()}')


##############################################
# import threading, queue

# def thread_function(q):
#     item = q.get()
#     print(f'Thread: {item}')

# def main():
# 	q = queue.Queue()

# 	q.put('one')
# 	q.put('two')
# 	q.put('three')

# 	# Create 3 threads - This is a list comprehension
# 	# Pass the queue as an argument to the threads
# 	threads = [threading.Thread(target=thread_function, args=(q, )) for _ in range(3)]

# 	# start all threads
# 	for i in range(3):
# 		threads[i].start()

# 	# Wait for them to finish
# 	for i in range(3):
# 		threads[i].join()

# 	print('All work completed')

# if __name__ == '__main__':
# 	main()

#######################################
# from multiprocessing import Process, Queue

# def f(q):
#     q.put('X' * 1000000)

# if __name__ == '__main__':
#     queue = Queue()
#     p = Process(target=f, args=(queue,))
#     p.start()
#     p.join()                    # this deadlocks
#     obj = queue.get()
    # this will deadlock. To fix it swap the last two lines

###############################################
# Ideally, don't use locks at all on critical sections. Risk of program becoming linear if locks are used too often
# Example 1
# import threading, time

# THREADS = 3
# ITEMS = 10000

# def thread_function(data):
#     for i in range(ITEMS):
#         data[0] += 1

# def main():    
#     data = [0]
#     start_time = time.perf_counter()

#     # Create threads
#     threads = [threading.Thread(target=thread_function, args=(data, )) for _ in range(THREADS)]

#     for t in threads:
#         t.start()

#     for t in threads:
#         t.join()

#     print(f'All work completed: {data[0]:,} in {time.perf_counter() - start_time:.5f} seconds')

# if __name__ == '__main__':
#     main()

# same as above but with 1,000,000 times
# Example 2
# import threading, time

# THREADS = 3
# ITEMS = 1000000

# def thread_function(data):
#     for i in range(ITEMS):
#         data[0] += 1

# def main():    
#     data = [0]
#     start_time = time.perf_counter()

#     # Create threads
#     threads = [threading.Thread(target=thread_function, args=(data, )) for _ in range(THREADS)]

#     for t in threads:
#         t.start()

#     for t in threads:
#         t.join()

#     print(f'All work completed: {data[0]:,} in {time.perf_counter() - start_time:.5f} seconds')

# if __name__ == '__main__':
#     main()

# uses a lock
# Example 3
# import threading, time

# THREADS = 3
# ITEMS = 1000000

# def thread_function(lock, data):
#     for i in range(ITEMS):
#         with lock:
#             data[0] += 1

# def main():    
#     lock = threading.Lock()
#     data = [0]
#     start_time = time.perf_counter()

#     # Create threads
#     threads = [threading.Thread(target=thread_function, args=(lock, data)) for _ in range(THREADS)]

#     for t in threads:
#         t.start()

#     for t in threads:
#         t.join()

#     print(f'All work completed: {data[0]:,} in {time.perf_counter() - start_time:.5f} seconds')

# if __name__ == '__main__':
#     main()    

# Example 4
# remove the race condition to fix the problem
# each thread gets its own variable index and those will be totaled at the end
# import threading, time

# THREADS = 3
# ITEMS = 1000000

# def thread_function(data, index):
#     for i in range(ITEMS):
#         data[index] += 1

# def main():    
#     data = [0] * THREADS   # Each thread uses it's own index into the list
#     start_time = time.perf_counter()

#     # Create threads
#     threads = [threading.Thread(target=thread_function, args=(data, index)) for index in range(THREADS)]

#     for t in threads:
#         t.start()

#     for t in threads:
#         t.join()

#     print(f'All work completed: {sum(data):,} in {time.perf_counter() - start_time:.5f} seconds')

# if __name__ == '__main__':
#     main()     

# Example 5
# using a shared queue between two threads
# the number of put() calls must match the number of get() calls or else you might/will have deadlock

'''

import threading
import queue

MAX_COUNT = 10

def read_thread(shared_q):
    for i in range(MAX_COUNT):
        # read from queue
        print(shared_q.get())

def write_thread(shared_q):
    for i in range(MAX_COUNT):
        # place value onto queue
        shared_q.put(i)

def main():
    """ Main function """

    shared_q = queue.Queue()

    write = threading.Thread(target=write_thread, args=(shared_q,))
    read = threading.Thread(target=read_thread, args=(shared_q,))

    read.start()        # doesn't matter which starts first
    write.start()

    write.join()		# Doesn't matter the order
    read.join()

if __name__ == '__main__':
    main()
'''
# for i in range(500):
#     car = Car()
#     # wasting resources
#     while q.size() < 10: 
#         q.add(car)

import threading

empty_spots = threading.Semaphore(10)
filled_spots = threading.Semaphore(0)

empty_spots + filled_spots == 10

if empty_spots._value > 0:
    pass

# acquire() ++ -> block 
# release() -- -> signal
