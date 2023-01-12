"""
Course: CSE 251
Lesson Week: 02 - Team Activity
File: team.py
Author: Brother Comeau

Purpose: Playing Card API calls

Instructions:

- Review instructions in I-Learn.

"""

from datetime import datetime, timedelta
import threading
import requests
import json

# Include cse 251 common Python files
from cse251 import *

# TODO Create a class based on (threading.Thread) that will
# make the API call to request data from the website

class Request_thread(threading.Thread):
    # TODO - Add code to make an API call and return the results
    # https://realpython.com/python-requests/
    # constructor
    def __init__(self, url):
        # calling parent class constructor
        threading.Thread.__init__(self)
        self.url = url
        self.response = {}

    # This is the method that is run when start() is called
    def run(self):
        response = requests.get(self.url)

        # Check the status code to see if the request succeeded.
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)

class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52


    def reshuffle(self):
        # TODO - add call to reshuffle DONE
        shuffle = Request_thread(rf'https://deckofcardsapi.com/api/deck/{self.id}/shuffle/')
        shuffle.start()
        shuffle.join()

    def draw_card(self):
        # TODO add call to get a card DONE
        draw = Request_thread(rf'https://deckofcardsapi.com/api/deck/{self.id}/draw/')
        draw.start()
        draw.join()
        if draw.response != {}:
            self.remaining = draw.response['remaining']
            return draw.response['cards'][0]['code']
        else:
            return ''

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
    # DONE

    deck_id = '0g3ffoyfx0ax'

    # Testing Code >>>>>
    deck = Deck(deck_id)
    for i in range(55):
        card = deck.draw_endless()
        print(i, card, flush=True)
    print()
    # <<<<<<<<<<<<<<<<<<

