import os
from aocd import get_data
import time


def get_input(day, token="\n"):
    "Open input file of corresponding day. Returns a list of strings"
    return get_data(day=day).split(token)


def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print ('%r  %2.20f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result
    return timed
