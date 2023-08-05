from operator import add, mul
from functools import reduce

def xsum(*args):
    return reduce(add, args)

def xmult(*args):
    return reduce(mul, args)
