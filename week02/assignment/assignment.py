"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class Request_thread(threading.Thread):
    # constructor
    def __init__(self, url):
        # calling parent class constructor
        threading.Thread.__init__(self)
        self.url = url
        self.response = {}

    # This is the method that is run when start() is called
    def run(self):
        response = requests.get(self.url)
        global call_count 
        call_count += 1
        # Check the status code to see if the request succeeded.
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)

# TODO Add any functions you need here
# Doesn't work
'''
def request_film_item(film_item, master_result_list):
  film_item_results = []
  for i in film_item:
    film_item_threads = Request_thread(i)
    # Append results to a list and put in a for loop---append is threadsafe
    film_item_results.append(film_item_threads)
    film_item_count = len(film_item_results)
  for i in film_item_results:
    master_result_list.append(i)
  return master_result_list
'''

def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')
    # make it work under 10 sec

    # TODO Retrieve Top API urls
    top = Request_thread(TOP_API_URL)
    top.start()
    top.join()
    top_response = top.response 
    # print(f'Top Details: {top_response}')
    # print("---")

    # TODO Retrieve Details on film 6
    # print(f'Films_URL:')
    # print(top_response['films'])
    # print("---")
    film6_url = top_response.get('films') + '6'
    film6_details = Request_thread(film6_url)
    film6_details.start()
    film6_details.join()
    # print("---")
    film6_all = film6_details.response
    # print(f'Film Six Details:')
    # print(film6_all)
    
    ### KEY ADDRESSES OF LISTS OF URL WE NEED TO LOOP THROUGH WITH THREADS
    characters = film6_all['characters']
    planets = film6_all['planets']
    starships = film6_all['starships']
    vehicles = film6_all['vehicles']
    species = film6_all['species']

    # DOESN'T WORK
    # request_film_item(characters, all_results)
    # request_film_item(planets, all_results)
    # request_film_item(starships, all_results)
    # request_film_item(vehicles, all_results)
    # request_film_item(species, all_results)

    ### MASTER RESULTS LIST
    all_results = []

    ### Loop through all the information in Film 6 using Request_thread(), append those threads to a topic list, and then append the topic list to the all_results master list. Also take note of the length of each topic list b/c you need that later for list slicing.
    # Characters 
    chara_results = []
    # print(characters)
    for i in characters:
      # print(i)
      chara_threads = Request_thread(i)
      chara_results.append(chara_threads)
      chara_count = len(chara_results)
    for i in chara_results:
      all_results.append(i)

    # Planets
    planet_results = []
    for i in planets:
      plan_threads = Request_thread(i)
      planet_results.append(plan_threads)
      planet_count = len(planet_results)
    for i in planet_results:
      all_results.append(i)

    # Starships
    starship_results = []
    for i in starships:
      star_threads = Request_thread(i)
      starship_results.append(star_threads)
      starship_count = len(starship_results)
    for i in starship_results:
      all_results.append(i)

    # Vehicles
    vehicle_results = []
    for i in vehicles:
      vehi_threads = Request_thread(i)
      vehicle_results.append(vehi_threads)
      vehicle_count = len(vehicle_results)
    for i in vehicle_results:
      all_results.append(i)

    # Species
    species_results = []
    for i in species:
      spec_threads = Request_thread(i)
      species_results.append(spec_threads)
      species_count = len(species_results)
    for i in species_results:
      all_results.append(i)

    ################################
    ### STARTING ALL THREADS
    for result in all_results:
      result.start()

    ################################
    ### JOINING THREADS, APPENDING RESULTS TO THE all_names MASTER LIST, SLICING INDICES FROM THE MASTER LIST, AND SORTING THE NEWLY SLICED LISTS
    ### ALL NAMES
    all_names = []
    for result in all_results:
      result.join()
      all_responses = result.response['name']
      all_names.append(all_responses)

    # print(f"All Names: {all_names}")
    character_names = all_names[0:chara_count]
    character_names.sort()
    # print(f"Character Names: {character_names}")

    planet_names_end = chara_count + planet_count
    planet_names = all_names[chara_count:planet_names_end]
    planet_names.sort()
    # print(f"Planet Names: {planet_names}")

    starship_names_end = planet_names_end + starship_count
    starship_names = all_names[planet_names_end:starship_names_end]
    starship_names.sort()
    # print(f"Starship Names: {starship_names}")

    vehicle_names_end = starship_names_end + vehicle_count
    vehicle_names = all_names[starship_names_end:vehicle_names_end]
    vehicle_names.sort()
    # print(f"Vehicle Names: {vehicle_names}")

    species_names_end = vehicle_names_end + species_count
    species_names = all_names[vehicle_names_end:species_names_end]
    species_names.sort()
    # print(f"Species Names: {species_names}")


    # TODO Display results
    title = film6_all['title']
    director = film6_all['director']
    producer = film6_all['producer']
    release_date = film6_all['release_date']

    log.write('-----------------------------------------')
    log.write('Title   : ' + title)
    log.write('Director: ' + director)
    log.write('Producer: ' + producer)
    log.write(f'Released: {release_date}' + '\n')

    log.write(f'Characters: {chara_count}')
    log.write(', '.join(character_names) + '\n')
    
    log.write(f'Planets: {planet_count}')
    log.write(', '.join(planet_names) + '\n')

    log.write(f'Starships: {starship_count}')
    log.write(', '.join(starship_names) + '\n')

    log.write(f'Vehicles: {vehicle_count}')
    log.write(', '.join(vehicle_names) + '\n')

    log.write(f'Species: {species_count}')
    log.write(', '.join(species_names) + '\n')


    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()
