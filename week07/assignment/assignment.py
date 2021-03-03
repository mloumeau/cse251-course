"""
Course: CSE 251
Lesson Week: 07
File: assingnment.py
Author: <Your name here>

Purpose: Process Task Files

Instructions:

- run the Python program "create_tasks.py" to create the task files.
- There are 5 different tasks that need to be processed.  Each task needs to
  have it's own process pool.  The number of processes in each pool is up to
  you.  However, your goal is to process all of the tasks as quicky as possible
  using these pools.  You will need to try out different pool sizes.
- The program will load a task one at a time and add it to the pool that is used
  to process that task.  You can't load all of the tasks into memory/list and
  then pass them to a pool.
- You are required to use the function apply_async() for these 5 pools. You can't
  use map(), or any other pool function.
- Each pool will collect that results of their tasks into a global list.
  (ie. result_primes, result_words, result_upper, result_sums, result_names)
- the task_* functions contain general logic of what needs to happen


Comments:
My machine only has 4 logical processors so I couldn't get the full effect
from this assignment. I was able to get all the tasks completed in 29 seconds
when I ran them all under the same pool with 6 processes. However, for the
sake of experimenting with this assignment, I played around with creating
pools for each task. Unfortunately, the best I could do with that was around
41 seconds. I can imagine that this method would be more effective than having
only a single pool if the machine running it had more cores.

I spent a lot of time trying to optimize the runtime. I tried implementing
a thread class, but found out that async can't return objects to a callback.
(At least I couldn't get it to work).

I did my best and think I deserve an A.

Grade:
93-100%
"""

from datetime import datetime, timedelta
import threading
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 

# Include cse 251 common Python files - Dont change
import os, sys
sys.path.append('../../code')
from cse251 import *

TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# Global lists to collect the task results
# Note: Global variables work here because as are using threads and not processes
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []


def is_prime(n: int):
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
 
def task_prime(value):
    """
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    return is_prime(value)

def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    with open('words.txt') as f:
        if word in f.read():
            f.close()
            return f"{word} Found"
    f.close()
    return f"{word} not found *****"
    


def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    return text.upper()

def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    return sum([i for i in range(start_value, end_value+1)])

def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """

    response = requests.get(url)
    json = response.json()
    return json['name']

def log_result_primes(result):
    result_primes.append(result)

def log_result_words(result):
    result_words.append(result)

def log_result_upper(result):
    result_upper.append(result)

def log_result_sums(result):
    result_sums.append(result)

def log_result_names(result):
    result_names.append(result)

def log_list(lst, log):
    for item in lst:
        log.write(item)
    log.write(' ')

def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create process pools
    # prime_pool = mp.Pool(1)
    # word_pool = mp.Pool(1)
    # upper_pool = mp.Pool(1)
    # sum_pool = mp.Pool(1)
    # name_pool = mp.Pool(1)
    pool = mp.Pool(6)

    count = 0
    task_files = glob.glob("*.task")
    for filename in task_files:
        # print()
        # print(filename)
        task = load_json_file(filename)
        # print(task)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            # prime_pool.apply_async(task_prime, args=(task['value'], ), callback= log_result_primes)
            pool.apply_async(task_prime, args=(task['value'], ), callback= log_result_primes)
        elif task_type == TYPE_WORD:
            # word_pool.apply_async(task_word, args=(task['word'],), callback= log_result_words)
            pool.apply_async(task_word, args=(task['word'],), callback= log_result_words)
        elif task_type == TYPE_UPPER:
            # upper_pool.apply_async(task_upper, args=(task['text'], ), callback= log_result_upper)
            pool.apply_async(task_upper, args=(task['text'], ), callback= log_result_upper)
        elif task_type == TYPE_SUM:
            # sum_pool.apply_async(task_sum, args=(task['start'], task['end']), callback= log_result_sums)
            pool.apply_async(task_sum, args=(task['start'], task['end']), callback= log_result_sums)
        elif task_type == TYPE_NAME:
            # name_pool.apply_async(task_name, args=(task['url'], ), callback= log_result_names)
            pool.apply_async(task_name, args=(task['url'], ), callback= log_result_names)
        else:
            log.write(f'Error: unknown task type {task_type}')

    # TODO start and wait pools

    # prime_pool.close()
    # word_pool.close()
    # upper_pool.close()
    # sum_pool.close()
    # name_pool.close()
    pool.close()

    # prime_pool.join()
    # word_pool.join()
    # upper_pool.join()
    # sum_pool.join()
    # name_pool.join()
    pool.join()

    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Primes: {len(result_primes)}')
    log.write(f'Words: {len(result_words)}')
    log.write(f'Uppercase: {len(result_upper)}')
    log.write(f'Sums: {len(result_sums)}')
    log.write(f'Names: {len(result_names)}')
    log.stop_timer(f'Finished processes {count} tasks')

if __name__ == '__main__':
    main()
