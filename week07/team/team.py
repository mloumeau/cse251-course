"""
Course: CSE 251
Lesson Week: Week 07
File: team.py
Author: Brother Comeau

Purpose: Week 05 Team Activity

Instructions:

- Make a copy of your assignment 2 program.  Since you are working in a team,
  you can design which assignment 2 program that you will use for the team
  activity.
- Convert the program to use a process pool and use apply_async() with a
  callback function to retrieve data from the Star Wars website.

"""


from datetime import datetime, timedelta
import requests
import json
import threading
import time
import multiprocessing as mp

# Include cse 251 common Python files
import os, sys
sys.path.append('../../code')
from cse251 import *

# Const Values
TOP_API_URL = 'https://swapi.dev/api/'

# Global Variables
call_count = 0
result_list = []


# TODO Add your threaded class definition here
class Request_thread(threading.Thread):
    def __init__(self,url):
        threading.Thread.__init__(self)
        self.response = ''
        self.url=url

    def run(self):
        response = requests.get(self.url)
        self.response=response.json()
        global call_count
        call_count += 1
        return

# TODO Add any functions you need here

#A dynamic function that creates a list of threads and returns them.

def getDetails(d,name):
  return [Request_thread(x) for x in d[name]]

def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from swapi.dev')

    pool = mp.Pool(4)


    # TODO Retrieve Top API urls
    topLevel = Request_thread(TOP_API_URL) # Can't mess with the original URL so this is necessary
    topLevel.start()
    topLevel.join()
    secondLevel = Request_thread(topLevel.response['films']) #Creates the json for all the films
    secondLevel.start()
    secondLevel.join()

    # TODO Retireve Details on film 6
    film = secondLevel.response['results'][int(input("Which movie would you like? (1-6)"))-1] # Creates the json for inputted movie
    pool = mp.Pool(4)

    #Collecting all the threads before starting them
    threads=[]

    for x in pool.apply_async(getDetails, args=(film,'characters')).get():
      threads.append(x)
    lenChar = len(threads)  #The lengths are here for slicing purposes in future loops
    for x in pool.apply_async(getDetails, args=(film,'planets')).get():
      threads.append(x)
    lenPlan = len(threads)
    for x in pool.apply_async(getDetails, args=(film,'starship')).get():
      threads.append(x)
    lenStar = len(threads)  
    for x in pool.apply_async(getDetails, args=(film,'vehicles')).get():
      threads.append(x)
    lenVeh = len(threads)
    for x in pool.apply_async(getDetails, args=(film,'species')).get():
      threads.append(x)
    lenSpec = len(threads)

    #Starting all the threads, joining all the threads
    [x.start() for x in threads]
    [x.join() for x in threads]

    pool.close()
    pool.join()
 
    #Creating lists of the names
    characters=[x.response['name'] for x in threads[:lenChar]]
    planets=[x.response['name'] for x in threads[lenChar:lenPlan]]
    starships=[x.response['name'] for x in threads[lenPlan:lenStar]]
    vehicles=[x.response['name'] for x in threads[lenStar:lenVeh]]
    species=[x.response['name'] for x in threads[lenVeh:lenSpec]]

    #Sorting the lists
    characters.sort()
    planets.sort()
    starships.sort()
    vehicles.sort()
    species.sort()

    # TODO Display results
    log.write("----------------------------------------")
    log.write('Title   : {}'.format(film['title']))
    log.write('Director: {}'.format(film['director']))
    log.write('Producer: {}'.format(film['producer']))
    log.write('Released: {}'.format(film['release_date']))

    log.write('')

    log.write("Characters: {}".format(len(characters)))
    log.write(", ".join(characters))
    
    log.write('')

    log.write("Planets: {}".format(len(planets)))
    log.write(", ".join(planets))

    log.write('')

    log.write("Starships: {}".format(len(starships)))
    log.write(", ".join(starships))

    log.write('')

    log.write("Vehicles: {}".format(len(vehicles)))
    log.write(", ".join(vehicles))

    log.write('')

    log.write("Species: {}".format(len(species)))
    log.write(", ".join(species))

    log.write('')

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to swapi server')
    

if __name__ == "__main__":
    main()
