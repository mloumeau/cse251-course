"""
Course: CSE 251
Lesson Week: 01 - Team Acvitiy
File: team.py
Author: Brother Comeau


Purpose: Find prime numbers

Instructions:

- Don't include any other Python packages or modules
- Review team acvitiy details in I-Learn

"""

from datetime import datetime, timedelta
import threading


# Include cse 251 common Python files
import os, sys
sys.path.append('C:\\Users\\matth\\OneDrive\\Desktop\\Winter 2021\\CSE251\\code')
from cse251 import *

# Global variable for counting the number of primes found
globalCount = 0
numbers_processed = 0
prime_count=0

def is_prime(n: int) -> bool:
    global numbers_processed
    numbers_processed += 1

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



def checkPrimeLoop(start, end):
    global globalCount
    for i in range(start, end):
        if is_prime(i):
            globalCount += 1
            print(i, end=', ', flush=True)

if __name__ == '__main__':
    log = Log(show_terminal=True)
    log.start_timer()

    start = 10000000000
    range_count = 100000
    # for i in range(start, start + range_count):
    #     if is_prime(i):
    #         prime_count += 1
    #         print(i, end=', ', flush=True)
    # print(flush=True)

    #create threads
    threadList=[]
    for i in range(10):
        thread = threading.Thread(target=checkPrimeLoop,args=(start + 10000*i,start + 10000*(i+1)))
        threadList.append(thread)
        
    #start threads
    for t in threadList:
        t.start()
    
    #join threads
    for t in threadList:
       t.join()


    # Should find 4306 primes
    log.write(f'Numbers processed = {numbers_processed}')
    log.write(f'Primes found      = {globalCount}')
    log.stop_timer('Total time')


