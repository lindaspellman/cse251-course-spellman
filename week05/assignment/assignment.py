"""
Course: CSE 251
Lesson Week: 05
File: assignment.py
Author: <Your name>

Purpose: Assignment 05 - Factories and Dealers

Instructions:

- Read the comments in the following code.  
- Implement your code where the TODO comments are found.
- No global variables, all data must be passed to the objects.
- Only the included/imported packages are allowed.  
- Thread/process pools are not allowed
- You are not allowed to use the normal Python Queue object.  You must use Queue251.
- the shared queue between the threads that are used to hold the Car objects
  can not be greater than MAX_QUEUE_SIZE

"""

from datetime import datetime, timedelta
import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Consts
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has was just created in the terminal
        self.display()
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []
        self.max_size = 0

    def get_max_size(self):
        return self.max_size

    def put(self, item):
        self.items.append(item)
        if len(self.items) > self.max_size:
            self.max_size = len(self.items)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, que, empty_spots, filled_spots, barrier, f, factory_stats, dealer_count):
        self.cars_to_produce = random.randint(200, 300)     # Don't change
        threading.Thread.__init__(self)
        self.que = que 
        self.empty_spots = empty_spots
        self.filled_spots = filled_spots
        self.barrier = barrier 
        self.id = f 
        self.factory_stats = factory_stats
        self.dealer_count = dealer_count

    def run(self):
        # TODO produce the cars, the send them to the dealerships
        for i in range(self.cars_to_produce):
            """
            create the cars
            place the car on the queue
            "signal" the dealer that there is a car on the queue
            """
            # acquire makes empty spots decrease by 1
            self.empty_spots.acquire()
            new_car = Car()
            self.factory_stats[self.id] += 1
            self.que.put(new_car)
            # release makes empty spots increase by 1
            self.filled_spots.release()

        # TODO wait until all of the factories are finished producing cars
        self.barrier.wait()

        # TODO "Wake up/signal" the dealerships one more time.  Select one factory to do this
        if (self.id == 0):
            for n in range(self.dealer_count):
                self.empty_spots.acquire()
                self.que.put("finished")
                self.filled_spots.release()
                
                # log.write("put finished")


class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, que, dealer_stats, empty_spots, filled_spots, d):
        threading.Thread.__init__(self)
        self.que = que 
        self.dealer_stats = dealer_stats
        self.empty_spots = empty_spots
        self.filled_spots = filled_spots
        self.id = d 

    def run(self):
        while True:
            # TODO handle a car
            # acquire makes empty spots decrease by 1
            self.filled_spots.acquire()
            self.dealer_stats[self.id] += 1
            # update queue_stats !!!!!!!!!!
            # sell the car by removing one from the queue
            car = self.que.get()
            if car == 'finished':
                self.dealer_stats[self.id] -= 1
                break 
            # release makes empty spots increase by 1
            self.empty_spots.release()

            # Sleep a little - don't change.  This is the last line of the loop
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR + 0))



def run_production(factory_count, dealer_count):
    """ This function will do a production run with the number of
        factories and dealerships passed in as arguments.
    """

    # TODO Create 2 semaphore(s)
    empty_spots = threading.Semaphore(MAX_QUEUE_SIZE)
    filled_spots = threading.Semaphore(0)
    # TODO Create 1 queue
    car_queue = Queue251()
    # TODO Create 1 barrier(s)
    barrier = threading.Barrier(factory_count)

    # This is used to track the number of cars receives by each dealer
    dealer_stats = list([0] * dealer_count)
    factory_stats = list([0] * factory_count)

    # TODO create your factories, each factory will create CARS_TO_CREATE_PER_FACTORY
    factories = []
    for f in range(factory_count):
        factory = Factory(car_queue, empty_spots, filled_spots, barrier,f, factory_stats, dealer_count)
        factories.append(factory)

    # TODO create your dealerships
    dealerships = [] 
    for d in range(dealer_count):
        dealer = Dealer(car_queue, dealer_stats, empty_spots, filled_spots, d)
        dealerships.append(dealer)

    log.start_timer()

    # TODO Start all dealerships
    for dealer in dealerships:
        dealer.start()

    time.sleep(1)   # make sure all dealers have time to start

    # TODO Start all factories
    for factory in factories:
        factory.start()
    
    # TODO Wait for factories and dealerships to complete
    for factory in factories:
        factory.join()

    for dealer in dealerships:
        dealer.join()

    run_time = log.stop_timer(f'{sum(dealer_stats)} cars have been created')

    # This function must return the following - Don't change!
    # factory_stats: is a list of the number of cars produced by each factory.
    #                collect this information after the factories are finished. 
    return (run_time, car_queue.get_max_size(), dealer_stats, factory_stats)


def main(log):
    """ Main function - DO NOT CHANGE! """

    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    for factories, dealerships in runs:
        run_time, max_queue_size, dealer_stats, factory_stats = run_production(factories, dealerships)

        log.write(f'Factories      : {factories}')
        log.write(f'Dealerships    : {dealerships}')
        log.write(f'Run Time       : {run_time:.4f}')
        log.write(f'Max queue size : {max_queue_size}')
        log.write(f'Factory Stats   : {factory_stats}')
        log.write(f'Dealer Stats   : {dealer_stats}')
        log.write('')

        # The number of cars produces needs to match the cars sold
        assert sum(dealer_stats) == sum(factory_stats)


if __name__ == '__main__':

    log = Log(show_terminal=True)
    main(log)


