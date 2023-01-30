import numpy as np
from functools import singledispatch
import pandas as pd

def vprint(*args):
    import inspect
    
    frame = inspect.currentframe()
    if 'verbose' in frame.f_back.f_locals:
        verbose = frame.f_back.f_locals['verbose']
    else:
        verbose = False
    
    if verbose: 
        for s in args[:(len(args)-1)]:
            print(s, end=' ')
        print(args[-1])
        
        
## Generic function to hash dictionary of various types

@singledispatch
## Top level hash function with built-in hash function for str, float, int, tuple, etc
def hash2(x):
    return hash(x)

@hash2.register(np.ndarray)
## Hash numpy array, hash array with pandas and return integer sum
def _(x):
    return hash(x.tobytes())

@hash2.register(list)
## Hash list, convert to tuple
def _(x):
    return hash2(tuple(x))

@hash2.register(tuple)
def _(x):
    r = 0
    for i in range(len(x)):
        r+=hash2(x[i])
    return r

@hash2.register(dict)
## Hash dict, loop through keys and hash each element via dispatch. Return hashed integer sum of hashes
def _(x, keys = None, verbose = False):
    r = 0 # return value integer
    if keys is None: # allow user input of keys to hash, otherwise hash them all
        keys = [*x.keys()]
    for key in keys:
        if (verbose): print('Hashing', key)
        r += hash2(x[key])
    return hash(r)