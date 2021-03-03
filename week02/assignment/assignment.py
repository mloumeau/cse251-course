"""
------------------------------------------------------------------------------
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a website

Instructions:

- each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information form the
  website.
- You are limited to about 10,000 calls to the swapi website.  That sounds like
  a lot, but you can reach this limit. If you leave this assignment to the last
  day it's due, you might be locked out of the website and you will have to
  submit what you have at that point.  There are no extensions because you
  reached this server limit. Work ahead and spread working on the assignment
  over multiple days.
- You need to match the output outlined in the dcription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the swapi server. You
  can define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary.  Do NOT have this
dictionary hard coded - use the API call to get this dictionary.  Then you can
use this dictionary to make other API calls for data.

{
   "people": "http://swapi.dev/api/people/", 
   "planets": "http://swapi.dev/api/planets/", 
   "films": "http://swapi.dev/api/films/",
   "species": "http://swapi.dev/api/species/", 
   "vehicles": "http://swapi.dev/api/vehicles/", 
   "starships": "http://swapi.dev/api/starships/"
}


IMPORTANT
This program requires user input.  If you want the 6th movie, input a 6.

For this assignment, I created a Request_Thread class that makes API calls,
and allows access to the JSON files. I created a dynamic function that allows
for multiple data types to be accessed. For each element in the data type 
json, a thread is created to make the API call for further information on
the element.  Once there, we only need the name, so that is what we call.

Once all threads are created, we make a new list and combine all the threads into
it.  When the list is full, only then to we start and join the threads.  This is
key to saving time.  From there, we created sublists from the threads list,
that only include the same data types (i.e. characters, planets etc.). Once
we have each of the lists, we can sort them.  All we have to do from there is
display the results.

The program is all dynamic, and not hardcoded. This means we could replace
the 6th movie with any other movie and the program would work just fine.
Because of this, I believe I deserve:
Grade: 100%
------------------------------------------------------------------------------
"""

from datetime import datetime, timedelta
import requests
import json
import threading
import time

# Include cse 251 common Python files
import os, sys
sys.path.append('../../code')
from cse251 import *

# Const Values
TOP_API_URL = 'https://swapi.dev/api/'

# Global Variables
call_count = 0



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

    # TODO Retrieve Top API urls
    topLevel = Request_thread(TOP_API_URL) # Can't mess with the original URL so this is necessary
    topLevel.start()
    topLevel.join()
    secondLevel = Request_thread(topLevel.response['films']) #Creates the json for all the films
    secondLevel.start()
    secondLevel.join()

    # TODO Retireve Details on film 6
    film = secondLevel.response['results'][int(input("Which movie would you like? (1-6)"))-1] # Creates the json for inputted movie

    #Collecting all the threads before starting them
    threads=[]
    for x in getDetails(film,'characters'):
      threads.append(x)
    lenChar = len(threads)  #The lengths are here for slicing purposes in future loops
    for x in getDetails(film,'planets'):
      threads.append(x)
    lenPlan = len(threads)
    for x in getDetails(film,'starships'):
      threads.append(x)
    lenStar = len(threads)  
    for x in getDetails(film,'vehicles'):
      threads.append(x)
    lenVeh = len(threads)
    for x in getDetails(film,'species'):
      threads.append(x)
    lenSpec = len(threads)

    #Starting all the threads, joining all the threads
    [x.start() for x in threads]
    [x.join() for x in threads]
 
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
