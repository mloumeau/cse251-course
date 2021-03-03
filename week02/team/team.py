"""
Course: CSE 251
Lesson Week: 02 - Team Activity
File: team.py
Author: Brother Comeau

Purpose: Playing Card API calls

Instructions:

- Don't include any other packages/modules.
- Use the website http://deckofcardsapi.com to implement then
  methods below.  Go to this website to get documentation on
  the API calls allowed.

"""

from datetime import datetime, timedelta
import threading
import requests
import json

# Include cse 251 common Python files
import os, sys
sys.path.append('C:\\Users\\matth\\OneDrive\\Desktop\\Winter 2021\\CSE251\\code')
from cse251 import *

# TODO Create a class based on (threading.Thread) that will
# make the API call to request data from the website

class Request_thread(threading.Thread):
    # TODO - Add code to make an API call and return the results
    # https://realpython.com/python-requests/
    def __init__(self,url):
        threading.Thread.__init__(self)
        self.id=deck_id
        self.response = ''
        self.url=url

    def run(self):
        response = requests.get(self.url)
        self.response = response.json()
        return

class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52


    def reshuffle(self):
        # TODO - add call to reshuffle
        t = Request_thread("https://deckofcardsapi.com/api/deck/j7yhl84145xs/shuffle/")
        t.start()
        t.join()
        return

    def draw_card(self):
        t = Request_thread("https://deckofcardsapi.com/api/deck/j7yhl84145xs/draw/?count=1")
        t.start()
        t.join()
        return t.response['cards'][0]['image']

    def cards_remaining(self):
        return self.remaining


    def draw_endless(self):
        if self.remaining <= 0:
            self.reshuffle()
        return self.draw_card()


if __name__ == '__main__':

    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the 
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = 'j7yhl84145xs'
    url = "https://deckofcardsapi.com/api/deck/j7yhl84145xs/"
    # Testing Code >>>>>

    a = Request_thread(url)
    a.start()
    a.join()
    print(a.response)

    # deck = Deck(deck_id)
    # for i in range(52):
    #     card = deck.draw_endless()
    #     print(i, card, flush=True)
    # <<<<<<<<<<<<<<<<<<

    # TODO once you have the functions above working, write a card game.
    # (ie., war, 31, UNO, etc...)
    # you can run the program "temp_get_deck_id.py" to get multiple decks
    # if you need them.
