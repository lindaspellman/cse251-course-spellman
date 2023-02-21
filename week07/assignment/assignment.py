"""
Course: CSE 251
Lesson Week: 07
File: assingnment.py
Author: Linda Spellman
Purpose: Process Task Files

Instructions:  See I-Learn

TODO

Add your comments here on the pool sizes that you used for your assignment and
why they were the best choices.
"""
# These are the best choices because ...
NUM_PRIME_POOLS = 1
NUM_WORD_POOLS = 2
NUM_UPPER_POOLS = 3
NUM_SUM_POOLS = 4
NUM_NAME_POOLS = 5


from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 

# Include cse 251 common Python files - Dont change
from cse251 import *

TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

final_results = {
    TYPE_PRIME: result_primes,
    TYPE_WORD: result_words,
    TYPE_UPPER: result_upper,
    TYPE_SUM: result_sums,
    TYPE_NAME: result_names
}

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
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    value = is_prime(value)
    if value == True:
        return (f"{value} is prime", TYPE_PRIME)
    else: 
        return (f"{value} is not prime", TYPE_PRIME)

def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    with open("words.txt", "r") as words:
        for w in words:
            if w == word:
                return (f"{word} Found", TYPE_WORD)
            else:
                return (f"{word} not Found", TYPE_WORD)

def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    text = text.upper()
    return (text, TYPE_UPPER)

def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    total = 0
    for i in range(start_value, end_value + 1):
        total += i
    return (total, TYPE_SUM)

def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    data = requests.get(url)
    # data.status_code
    # name = data["people1"]["name"]

    if data.status_code == 200:
    
    # if name in data:
        return (f"{url} has name <name>", TYPE_NAME)
    else:
        return (f"{url} had an error receiving the information", TYPE_NAME)


def callback(data):
    result, key = data
    final_results[key].append(result)


def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create process pools
    task_prime_pool = mp.Pool(NUM_PRIME_POOLS)
    task_word_pool = mp.Pool(NUM_WORD_POOLS)
    task_upper_pool = mp.Pool(NUM_UPPER_POOLS)
    task_sum_pool = mp.Pool(NUM_SUM_POOLS)
    task_name_pool = mp.Pool(NUM_NAME_POOLS)

    count = 0
    task_files = glob.glob("*.task")
    for filename in task_files:
        # print()
        # print(filename)
        task = load_json_file(filename)
        print(task)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            task_prime_pool.apply_async(task_prime, args=(task['value'], ), callback=callback)
        elif task_type == TYPE_WORD:
            task_word_pool.apply_async(task_word, args=(task['word'], ), callback=callback)
        elif task_type == TYPE_UPPER:
            task_upper_pool.apply_async(task_upper, args=(task['text'], ), callback=callback)
        elif task_type == TYPE_SUM:
            task_sum_pool.apply_async(task_sum, args=(task['start'], task['end'], ), callback=callback)
        elif task_type == TYPE_NAME:
            task_name_pool.apply_async(task_name, args=(task['url'], ), callback=callback)
        else:
            log.write(f'Error: unknown task type {task_type}')

    # TODO start and wait pools

    task_prime_pool.close()
    task_word_pool.close()
    task_upper_pool.close()
    task_sum_pool.close() 
    task_name_pool.close()

    task_prime_pool.join()
    task_word_pool.join()
    task_upper_pool.join()
    task_sum_pool.join() 
    task_name_pool.join()

    # Do not change the following code (to the end of the main function)
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
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

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Finished processes {count} tasks')

if __name__ == '__main__':
    main()
