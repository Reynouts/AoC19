import os


def get_input(day, token="\n"):
    "Open input file of corresponding day."
    with open('day{}.txt'.format(day), 'r') as myfile:
        data = myfile.read()
    return data.split(token)


def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
