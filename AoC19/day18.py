import aocutils as util
import copy
import os
import time
from random import randint
import msvcrt
import pickle

solutions = []
sol = 10*100

def draw(grid, refresh=False):
    result = ""
    for row in grid:
        for item in row:
            if item is "/":
                result += "#"
            else:
                result += item
        result += "\n"
    if refresh:
        time.sleep(0.1)
        os.system("cls")
    print(result)


def findstartpoint(grid, symbol):
    for j, row in enumerate(grid):
        for i, item in enumerate(row):
            if item is symbol:
                return (j,i)





def floodfill(grid, start, loper = False, depth=0):
    visited = set()
    visited.add(start)
    keycards = {}
    doors = {}
    while depth == 0 or len(neighbours) > 0:
        neighbours = set()
        for v in visited:
            x, y = v
            directions = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            for d in directions:
                if grid[d[0]][d[1]] in ".@":
                    if d not in visited:
                        neighbours.add(d)
                elif grid[d[0]][d[1]].islower():
                    keycards[grid[d[0]][d[1]]] = d
                    if d not in visited:
                        neighbours.add(d)
                elif grid[d[0]][d[1]].isupper():
                    doors[grid[d[0]][d[1]]] = d
                    if loper:
                        if d not in visited:
                            neighbours.add(d)
        for n in neighbours:
            visited.add(n)
        depth += 1
    return keycards, doors


def recur(sleutelhanger, keys_to_key, total_cost, cost, key):
    global solutions
    total_cost += cost
    sleutelhanger.add(key)
    current = key
    print(current, sleutelhanger, total_cost, solutions)
    if len(sleutelhanger) == 52:
        solutions.append(total_cost)
        print("solution found with cost: {}".format(total_cost))
        return total_cost

    for s in solutions:
        if s <= total_cost:
            return

    key_to_key = []

    for i, x in enumerate(keys_to_key):
        if x[0] == current:
            key_to_key = keys_to_key[i]
            break
    for path in key_to_key[1]:
        if path[1] not in sleutelhanger:
            if all(key in sleutelhanger for key in path[2]):
                print("from {}, can reach: {}".format(current, path[1]))

                cost, key, _ = path
                total_cost += cost
                sleutelhanger.add(key)
                sleutelhanger.add(key.upper())
                current = key
                recur(sleutelhanger, keys_to_key, total_cost, cost, key)


def pathfind(grid, start, end, visited, doors, depth=0):
    global sol
    if depth > sol:
        return (depth, doors.copy())
    visited.add(start)
    x, y = start
    if grid[x][y] == end:
        if depth <= sol:
            sol = depth
        return (depth, doors.copy())
    directions = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    endpoints = []
    for d in directions:
        _doors = doors.copy()
        if d not in visited:
            if grid[d[0]][d[1]] in ".@" or grid[d[0]][d[1]].isalpha():
                if d is not end.upper():
                    if grid[d[0]][d[1]].isupper():
                        #doors[grid[d[0]][d[1]]] = d
                        _doors.add(grid[d[0]][d[1]])
                    endpoints.append(pathfind(grid, d, end, visited.copy(), _doors.copy(), depth+1))
    if endpoints == []:
        return (10*100, set("<"))
    else:
        return min(endpoints)

@util.timeit
def main():
    with open("day18.txt", "r") as f:
        data = f.read().split("\n")
    data = [list(x) for x in data]
    draw(data)
    start = findstartpoint(data, "@")
    keycards, doors = floodfill(data, start, True)



    # # getting map from every key to every other key

    # global sol
    # start_to_key = [start, []]
    # visited = set()
    # doors = set()
    # for key in keycards.keys():
    #     sol = 10 * 100
    #     steps, doors = pathfind(data, start, key, visited.copy(), doors)
    #     #start_to_key[1].append((steps, key, [x for x in doors.keys()]))
    #     start_to_key[1].append((steps, key, doors))
    #
    # start_to_key[1] = sorted(start_to_key[1])
    #
    #
    #
    # keys_to_key = []
    # for key1 in keycards:
    #     doors = set()
    #     visited = set()
    #     key_to_key = [key1, []]
    #     for key2 in keycards.keys():
    #         sol = 10*100
    #         steps, doors = pathfind(data, keycards[key1], key2, visited.copy(), doors)
    #         #key_to_key[1].append((steps, key2, [x for x in doors.keys()]))
    #         key_to_key[1].append((steps, key2, doors))
    #
    #         #print(steps, key, doors.keys())
    #         #start = findstartpoint(data, key)
    #     keys_to_key.append(key_to_key)
    #
    # for k in keys_to_key:
    #     k[1] = sorted(k[1])
    #
    # with open("keys.txt", "wb") as fp:  # Pickling
    #     pickle.dump(keys_to_key, fp)
    #     pickle.dump(start_to_key, fp)


    with open("keys.txt", "rb") as fp:  # Unpickling
        keys_to_key = pickle.load(fp)
        start_to_key = pickle.load(fp)

    print(start_to_key)

    sleutelhanger = set()
    total_cost = 0
    print (start_to_key[1][0])
    cost, key, needed = start_to_key[1][0]

    print (cost, key, needed)
    global solutions

    recur(sleutelhanger, keys_to_key, total_cost, cost, key)

    print(solutions)
    # total_cost += cost
    # sleutelhanger.add(key)
    # current = key
    #
    # key_to_key = []
    #
    # while (len(sleutelhanger) < 26):
    #     #print ("Sleutelhanger ({}): {}".format(len(sleutelhanger), str(sleutelhanger)))
    #     for i, x in enumerate(keys_to_key):
    #         if x[0] == current:
    #             key_to_key = keys_to_key.pop(i)
    #             print (key_to_key)
    #             input()
    #             break
    #     for path in key_to_key[1]:
    #         print (path)
    #         input()
    #         if path[1] not in sleutelhanger:
    #             if all(key in sleutelhanger for key in path[2]):
    #                 cost, key, _ = path
    #                 total_cost += cost
    #                 sleutelhanger.add(key)
    #                 current = key
    #                 print ("current {}".format(current))
    #                 break
    #
    # print(total_cost)


# Part 1: 4620
# Part 2: 1564

if __name__ == "__main__":
    main()
