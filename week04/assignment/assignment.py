"""
Course: CSE 251
Lesson Week: 04
File: assignment.py
Author: Brother Comeau

Purpose: Assignment 04 - Factory and Dealership

Instructions:

- Read the comments in the following code.  
- Implement your code where the TODO comments are found.
- No global variables, all data must be passed to the objects.
- Only the included/imported packages are allowed.  
- Thread pools are not allowed
- the shared queue between the threads that are used to hold the Car objects
  can not be greater than MAX_QUEUE_SIZE

This assignment was a bit tricky. After giving it an effort, I worked with Jack
and he helped me understand semaphores a bit better. I believe I did everything
correctly, however the outputs vary each run. I think this is due to the
"approximate size" of the qsize() function.

I believe my grade should be:
Category 4-5
93-100%
"""

import time
import queue
import threading
import random

# Include cse 251 common Python files
import os, sys
sys.path.append('../../code')
from cse251 import *

# Global Consts - Do not change
CARS_TO_PRODUCE = 500
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
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')



class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, car_queue, full, empty,queue_stats):
        # TODO, you need to add arguments that will pass all of data that 1 factory needs
        # to create cars and to place them in a queue.
        threading.Thread.__init__(self)
        self.empty = empty
        self.full = full
        self.car_queue = car_queue
        self.car_count = CARS_TO_PRODUCE
        self.queue_stats = queue_stats
    def run(self):
        for i in range(self.car_count):
            # TODO Create a Car object and place it on a queue for the dealerships
            self.queue_stats[self.car_queue.qsize()] +=1
            self.empty.acquire()
            self.car_queue.put(Car())
            # Sleep a little - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR + 4))
            self.full.release()



class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, car_queue, full, empty, queue_stats):
        # TODO, you need to add arguments that pass all of data that 1 factory needs
        # to create cars and to place them in a queue
        threading.Thread.__init__(self)
        self.empty = empty
        self.full = full
        self.car_queue = car_queue
        self.queue_stats = queue_stats

    def run(self):
        while True:
            # TODO process a car if there is one
            if sum(self.queue_stats) >= CARS_TO_PRODUCE and self.car_queue.empty():
                break
            self.full.acquire()
            self.car_queue.get()
            # Sleep a little - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR + 0))
            self.empty.release()




def main():
    log = Log(show_terminal=True)

    # TODO Create semaphore(s) ?
    full = threading.Semaphore(0)
    empty = threading.Semaphore(MAX_QUEUE_SIZE)

    # TODO Create queue(s) ?
    car_queue=queue.Queue()

    # This tracks the length of the car queue during receiving cars by the dealership
    # i.e., update this list each time the dealer receives a car
    queue_stats = [0] * MAX_QUEUE_SIZE

    # TODO create your one factory
    fact = Factory(car_queue,full,empty,queue_stats)

    # TODO create your one dealership
    deal = Dealer(car_queue,full,empty,queue_stats)

    log.start_timer()

    # TODO Start factory and dealership
    fact.start()
    deal.start()


    # TODO Wait for factory and dealership to complete
    deal.join()
    fact.join()

    log.stop_timer(f'All {sum(queue_stats)} have been created')

    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')



if __name__ == '__main__':
    main()
