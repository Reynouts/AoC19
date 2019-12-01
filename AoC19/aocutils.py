import os
from aocd import get_data


def get_input(day, token="\n"):
    "Open input file of corresponding day. Returns a list of strings"
    return get_data(day=day).split(token)


def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
