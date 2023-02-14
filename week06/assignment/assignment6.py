"""
Course: CSE 251
Lesson Week: 06
File: assignment.py
Author: Linda Spellman
Purpose: Processing Plant
Instructions:
- Implement the classes to allow gifts to be created.
"""

import random
import multiprocessing as mp
import os.path
import time
import datetime

# Include cse 251 common Python files - Don't change
from cse251 import *

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME   = 'boxes.txt'

# Settings consts
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
BAG_COUNT = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables

class Bag():
    """ bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

class Gift():
    """ Gift of a large marble and a bag of marbles - Don't change """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, parent, count, delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.parent = parent 
        self.marble_count = count 
        self.creator_delay = delay 
        

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        for i in range(self.marble_count):
            marble = random.choice(Marble_Creator.colors)
            self.parent.send(marble)
            time.sleep(random.random() / (self.creator_delay + 0))
            
            # if i == -1:
            #     more_marbles = False

class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self, child, parent, delay, marble_count, bag_count):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.bagger_child = child 
        self.bagger_parent = parent
        self.bagger_delay = delay
        self.marble_count = marble_count
        self.bag_count = bag_count 

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        # find whole number part of decimal number of marbles per bag for the bag count minus one bag. Reminder: % finds remainder.
        int_marbles_per_bag = self.marble_count // self.bag_count - 1
        # find remaining number of marbles for the last bag
        remainder_marbles = self.marble_count - (int_marbles_per_bag * (self.bag_count - 1))

        bags_sent = 0

        unprocessed_bags = True
        while unprocessed_bags: 
            marble = self.bagger_child.recv()
            # collect enough marbles for a bag before sending
            for i in range(self.bag_count):
                bag = Bag()
                bag.add(marble)
                bag_size = bag.get_size()
                if bag_size == int_marbles_per_bag:
                    bag.add("done_marble")
                    self.bagger_parent.send(bag) 

            last_bag = Bag()
            last_bag.add(marble)
            bag_size = bag.get_size()
            if bag_size == remainder_marbles:
                self.bagger_parent.send(bag) 
           
            # sleep the required amount
            time.sleep(random.random() / (self.bagger_delay + 0))
            # tell the assembler that there are no more bags            
            unprocessed_bags = False 
        


class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'Master Luc', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, child, parent, delay, gift_count, bag_count):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.assembler_child = child 
        self.assembler_parent = parent
        self.assembler_delay = delay 
        self.gift_count = gift_count 
        self.bag_count = bag_count 

    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        unassembled_gifts = True 
        while unassembled_gifts:
            bag = self.assembler_child.recv()
            large_marble = random.choice(Assembler.marble_names)
            gift = Gift(large_marble, bag)
            self.gift_count += 1 
            self.assembler_parent.send(gift)
            time.sleep(random.random() / (self.assembler_delay + 0))
            # tell the wrapper that there are no more gifts
            if self.gift_count == self.bag_count: 
                unassembled_gifts = False 
        # return self.gift_count
        


class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """
    def __init__(self, child, delay, gift_count, bag_count):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.wrapper_child = child 
        self.wrapper_delay = delay
        self.gift_count = gift_count 
        self.bag_count = bag_count 

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''
        unwrapped_gifts = True
        with open("boxes.txt", "w") as box_file:
            while unwrapped_gifts:
                received_gifts = self.wrapper_child.recv()
                box_file.write(f"Created - {datetime.now().time()}: {received_gifts}")
                time.sleep(random.random() / (self.wrapper_delay + 0))
                if self.gift_count == self.bag_count:
                    unwrapped_gifts = False 

def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')



def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count     = {settings[MARBLE_COUNT]}')
    log.write(f'Marble delay     = {settings[CREATOR_DELAY]}')
    log.write(f'Bag count        = {settings[BAG_COUNT]}') 
    log.write(f'Bagger delay     = {settings[BAGGER_DELAY]}')
    log.write(f'Assembler delay  = {settings[ASSEMBLER_DELAY]}')
    log.write(f'Wrapper delay    = {settings[WRAPPER_DELAY]}')

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper
    creator_parent, bagger_child = mp.Pipe()
    bagger_parent, assembler_child = mp.Pipe()
    assembler_parent, wrapper_child = mp.Pipe()

    # TODO create variable to be used to count the number of gifts
    gift_count = 0 

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    marble_count = settings[MARBLE_COUNT]
    creator_delay = settings[CREATOR_DELAY]
    bag_count = settings[BAG_COUNT]
    bagger_delay = settings[BAGGER_DELAY]
    assembler_delay = settings[ASSEMBLER_DELAY]
    wrapper_delay = settings[WRAPPER_DELAY]

    # TODO Create the processes (i.e., classes above)
    creator = Marble_Creator(creator_parent, marble_count, creator_delay)
    bagger = Bagger(bagger_child, bagger_parent, bagger_delay, marble_count, bag_count)
    assembler = Assembler(assembler_child, assembler_parent, assembler_delay, gift_count, bag_count)
    wrapper = Wrapper(wrapper_child, wrapper_delay, gift_count, bag_count)

    log.write('Starting the processes')
    # TODO add code here
    creator.start()
    bagger.start()
    assembler.start()
    wrapper.start() 
    

    log.write('Waiting for processes to finish')
    # TODO add code here
    creator.join()
    log.write("creator joined")
    bagger.join()
    log.write("bagger joined")
    assembler.join()
    log.write("assembler joined")
    wrapper.join()
    log.write("wrapper joined")


    display_final_boxes(BOXES_FILENAME, log)
    
    # TODO Log the number of gifts created.
    log.write(f"Number of Gifts Created: {gift_count}")



if __name__ == '__main__':
    main()

