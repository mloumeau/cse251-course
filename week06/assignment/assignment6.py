"""
Course: CSE 251
Lesson Week: 06
File: assignment.py
Author: Brother Comeau

Purpose: Processing Plant

Instructions:

- Implement the classes to allow gifts to be created.

I had to change a couple of minor things. Some of the
variables were defined outside of the init function,
so to make things easier I just made them a member
variable. Another thing I changed was the Gift class.
I added the time as a parameter, and included it in 
the str function. This allows for easy record-keeping
of when each gift was created by passing in the time
when the object is made.

Overall, the pipes work well. Each one sends its
info to the connecting pipe. The pipes overlap
for the different classes and work together.

Grade:
93-100%

"""

from datetime import datetime, timedelta
import random
import json
import threading
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import os.path
import datetime
import time

# Include cse 251 common Python files - Don't change
import os, sys
sys.path.append('../../code')
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
    """ bag of marbles - Don't change for the 93% """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


class Gift():
    """ Gift of a large marble and a bag of marbles - Don't change for the 93% """

    def __init__(self, time, large_marble, marbles):
        self.currentTime = time
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Created - {self.currentTime} Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """



    def __init__(self, pipeConn, marbCount, delay):
        self.colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
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
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.marbCount = marbCount
        self.pipeConn = pipeConn
        self.delay = delay

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        for _ in range(self.marbCount):
            self.pipeConn.send(random.choice(self.colors))
            time.sleep(self.delay)
        self.pipeConn.send("ALL DONE!")
        self.pipeConn.close()


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self, fromCreator, toAssembler, bagCount, delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.fromCreator = fromCreator
        self.toAssembler = toAssembler
        self.bagCount = bagCount
        self.delay = delay

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        bagList=[]
        while True:
            bag = Bag()
            for _ in range(self.bagCount):
                marble = self.fromCreator.recv()
                if marble != "ALL DONE!":
                    bag.add(marble)
                    # print(marble)
                    time.sleep(self.delay)
                else:
                    self.toAssembler.send(bagList)
                    self.fromCreator.close()
                    self.toAssembler.close()
                    return
            bagList.append(bag)

            
class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """

    def __init__(self, fromBag, toWrapper, delay, numGifts):
        self.marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'The Boss', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.fromBag = fromBag
        self.toWrapper = toWrapper
        self.delay = delay
        self.numGifts = numGifts

    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        giftList=[]
        for bag in self.fromBag.recv():
            # print(bag)
            gift = Gift(datetime.now().time(), random.choice(self.marble_names),bag)
            time.sleep(self.delay)
            self.numGifts.value += 1
            giftList.append(gift)
        self.toWrapper.send(giftList)
        self.fromBag.close()
        self.toWrapper.close()

class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """
    def __init__(self, fromAssembler,fileName, delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.fromAssembler = fromAssembler
        self.fileName = fileName
        self.delay = delay

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''
        with open(self.fileName, "x") as f:
            for x in self.fromAssembler.recv():
                f.write(str(x))
                f.write("\n")
                time.sleep(self.delay)
        f.close()
        self.fromAssembler.close()


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

    log.write(f'Marble count                = {settings[MARBLE_COUNT]}')
    log.write(f'settings["creator-delay"]   = {settings[CREATOR_DELAY]}')
    log.write(f'settings["bag-count"]       = {settings[BAG_COUNT]}') 
    log.write(f'settings["bagger-delay"]    = {settings[BAGGER_DELAY]}')
    log.write(f'settings["assembler-delay"] = {settings[ASSEMBLER_DELAY]}')
    log.write(f'settings["wrapper-delay"]   = {settings[WRAPPER_DELAY]}')

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper
    parent_conn_creator,child_conn_creator = mp.Pipe()
    parent_conn_bagger,child_conn_bagger = mp.Pipe()
    parent_conn_assembler,child_conn_assembler = mp.Pipe()


    # TODO create variable to be used to count the number of gifts
    numGifts = mp.Value('i', 0)

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    # TODO Create the processes (ie., classes above)
    start_creator = Marble_Creator(parent_conn_creator, settings[MARBLE_COUNT], settings[CREATOR_DELAY])
    start_bagger = Bagger(child_conn_creator, parent_conn_bagger, settings[BAG_COUNT], settings[BAGGER_DELAY])
    start_assembler = Assembler(child_conn_bagger, parent_conn_assembler, settings[ASSEMBLER_DELAY], numGifts)
    start_wrapper = Wrapper(child_conn_assembler, BOXES_FILENAME, settings[WRAPPER_DELAY])

    log.write('Starting the processes')

    # TODO add code here
    start_creator.start()
    start_bagger.start()
    start_assembler.start()
    start_wrapper.start()

    log.write('Waiting for processes to finish')

    # TODO add code here
    start_creator.join()
    start_bagger.join()
    start_assembler.join()
    start_wrapper.join()

    display_final_boxes(BOXES_FILENAME, log)

    # TODO Log the number of gifts created.
    log.write(f"Number of gifts - {numGifts.value}")


if __name__ == '__main__':
    main()

