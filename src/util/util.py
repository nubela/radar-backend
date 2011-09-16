#===============================================================================
# General Util Module
# / steven 9th sep
#===============================================================================

import string
from random import choice, randint
import json
 
# The characters to make up the random password
chars = string.ascii_letters + string.digits
 
def random_string():
    """ Create a string of random length between 8 and 16
        characters long, made up of numbers and letters.
    """
    return "".join(choice(chars) for x in range(randint(8, 16)))

    
def json_wrapper(dict):
    """
    Just a nice wrapper around the json module with nice sane defaults..
    """
    return json.dumps(dict, sort_keys=True, indent=4)

def fib():
    i = 0
    j = 1
    yield i
    yield j
    while True:
        yield i+j
        k = j
        j = i+j
        i = k
    