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
# def add_to_thread_safe_dict(dict, key, val):
#   lock = threading.Lock() 
#   with lock:
#     dict[key] = val 

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

    # for i in film6_all:
    #   # print(i)
    #   print("---")
    #   print(i + ': ')
    #   print(film6_all[i])
    
    ### Get all the information in Film 6 using Request_thread() and append those threads to the results lists.
    # full_list = {}
    all_results = []
    # Characters 
    chara_results = []
    characters = film6_all['characters']
    # print(characters)
    for i in characters:
      # print(i)
      chara_threads = Request_thread(i)
      # append results to a list and put in a for loop---append is threadsafe
      chara_results.append(chara_threads)
      chara_count = len(chara_results)
    for i in chara_results:
      all_results.append(i)
      # chara_thread = threading.Thread(target=add_to_thread_safe_dict, args=(full_list, 'characters', i))
      # full_list['characters'] = i
      # full_list.append(chara_results)
    # print(chara_results)

    # Planets
    planet_results = []
    planets = film6_all['planets']
    for i in planets:
      plan_threads = Request_thread(i)
      planet_results.append(plan_threads)
      planet_count = len(planet_results)
    for i in planet_results:
      all_results.append(i)
      # planet_thread = threading.Thread(target=add_to_thread_safe_dict, args=(full_list, 'planets', i))
      # full_list['planets'] = i

    # Starships
    starship_results = []
    starships = film6_all['starships']
    for i in starships:
      star_threads = Request_thread(i)
      starship_results.append(star_threads)
      starship_count = len(starship_results)
    for i in starship_results:
      all_results.append(i)
      # starship_thread = threading.Thread(target=add_to_thread_safe_dict, args=(full_list, 'starships', i))
      # full_list['starships'] = i

    # Vehicles
    vehicle_results = []
    vehicles = film6_all['vehicles']
    for i in vehicles:
      vehi_threads = Request_thread(i)
      vehicle_results.append(vehi_threads)
      vehicle_count = len(vehicle_results)
    for i in vehicle_results:
      all_results.append(i)
      # vehicle_thread = threading.Thread(target=add_to_thread_safe_dict, args=(full_list, 'vehicles', i))
      # full_list['vehicles'] = i

    # Species
    species_results = []
    species = film6_all['species']
    for i in species:
      spec_threads = Request_thread(i)
      species_results.append(spec_threads)
      species_count = len(species_results)
    for i in species_results:
      all_results.append(i)
      # species_thread = threading.Thread(target=add_to_thread_safe_dict, args=(full_list, 'species', i))
      # full_list['species'] = i


    ### Append the Sorted Lists to a Full List
    ################################
    ### STARTING THREADS
    ### Characters
    for result in all_results:
      result.start()

    # for c in chara_results:
    #   c.start()

    # ### Planets
    # for p in planet_results:
    #   p.start()

    # ### Starships
    # for s in starship_results:
    #   s.start()

    # ### Vehicles
    # for v in vehicle_results:
    #   v.start()

    # ### Species
    # for s in species_results:
    #   s.start()

    ################################
    ### JOINING THREADS
    all_names = []
    for result in all_results:
      result.join()
      all_responses = result.response['name']
      # all_responses.split(", ")
      # print(all_responses)
    # for response in all_responses:
      # print(response)
      all_names.append(all_responses)
    print(all_names)


    ### For each character thread in the chara_results thread list, join it to the main thread. Get the name value from each chara thread and append it to the people list.
    # people = []
    # for chara in chara_results:
    #   chara.join() 
    #   character_list = chara.response['name']
    #   people.append(character_list)
    #   # print(character_list)

    # For each character thread in the chara_results thread list, join it to the main thread. Get the name value from each chara thread and append it to the people list.
    # planet_list = []
    # for planet in planet_results:
    #   planet.join()
    #   planet_names = planet.response['name']
    #   planet_list.append(planet_names)

    # # Starships
    # starship_list = []
    # for starship in starship_results:
    #   starship.join()
    #   starship_names = starship.response['name']
    #   starship_list.append(starship_names)

    # # Vehicles
    # vehicle_list = []
    # for vehicle in vehicle_results:
    #   vehicle.join()
    #   vehicle_names = vehicle.response['name']
    #   vehicle_list.append(vehicle_names)

    # # Species
    # species_list = []
    # for specie in species_results:
    #   specie.join()
    #   species_names = specie.response['name']
    #   species_list.append(species_names)

    ### SORT THE LISTS
    people = []
    for i in all_names:
      # i.split(",")
      # print(i)
      for j in characters:
        if i == j:
          people.append(i)
          # print(i)
    people.sort()
    # print(people) # This currently doesn't work.

    planet_output = []
    for i in all_names:
      # i.split(",")
      # print(i)
      for j in planets:
        if i == j:
          planet_output.append(i)
          # print(i)
    planet_output.sort()

    starship_output = []
    for i in all_names:
      # i.split(",")
      # print(i)
      for j in starships:
        if i == j:
          starship_output.append(i)
          # print(i)
    starship_output.sort()

    vehicle_output = []
    for i in all_names:
      # i.split(",")
      # print(i)
      for j in vehicles:
        if i == j:
          vehicle_output.append(i)
          # print(i)
    vehicle_output.sort()

    species_output = []
    for i in all_names:
      # i.split(",")
      # print(i)
      for j in species:
        if i == j:
          species_output.append(i)
          # print(i)
    species_output.sort()
    # print(planet_output) # This currently doesn't work.
    # starship_list.sort()
    # vehicle_list.sort()
    # species_list.sort()

    # for i in film6_all['characters']:
    #     characters = Request_thread(i)
    #     characters.start()
    #     characters.join()
    #     charas = characters.response

    # for i in charas:
    #     print(charas)

      
    # for i in results:
      ##### create threads

    # TODO Display results
    title = film6_all['title']
    director = film6_all['director']
    producer = film6_all['producer']
    release_date = film6_all['release_date']

    log.write('Title   : ' + title)
    log.write('Director: ' + director)
    log.write('Producer: ' + producer)
    log.write(f'Released: {release_date}')

    log.write(f'Characters: {chara_count}')
    log.write(', '.join(people) + '\n')
    
    log.write(f'Planets: {planet_count}')
    log.write(', '.join(planet_output) + '\n')

    log.write(f'Starships: {starship_count}')
    log.write(', '.join(starship_output) + '\n')

    log.write(f'Vehicles: {vehicle_count}')
    log.write(', '.join(vehicle_output) + '\n')

    log.write(f'Species: {species_count}')
    log.write(', '.join(species_output) + '\n')


    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()
