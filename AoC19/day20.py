import copy
import os
import aocutils as util
from collections import defaultdict

WIDTH = 0
HEIGHT = 0


def draw(tiles):
    result = ""
    for j in range(HEIGHT):
        for i in range(WIDTH):
            if (i, j) in tiles:
                result += tiles[i, j]
            else:
                result += " "
        result += "\n"
    print(result)


def in_outer(pos):
    if pos[0] <= 3 or pos[0] >= WIDTH-3:
        return True
    if pos[1] <= 3 or pos[1] >= HEIGHT-3:
        return True
    return False


def get_teleport_exit(pos, teleports):
    if pos in teleports[0]:
        return teleports[1][teleports[0].index(pos)]
    elif pos in teleports[1]:
        return teleports[0][teleports[1].index(pos)]
    else:
        raise ValueError


def surrounding(tiles, pos, teleports=None):
    x, y = pos
    directions = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    neighbours = {}
    for d in directions:
        if d in tiles:
            neighbours[d] = tiles[d]
    if pos in tiles and tiles[pos] == "*" and teleports:
        get_teleport_exit(pos, teleports)
    return neighbours


def get_teleport_location(tiles, positions):
    for p in positions:
        s = surrounding(tiles, p)
        for t in s:
            if s[t] == ".":
                return t


def make_pairs(tiles, letters):
    couples = []
    for l1 in letters:
        for l2 in letters:
            if l1 is not l2:
                if abs(l1[1][0] - l2[1][0]) + abs(l1[1][1] - l2[1][1]) == 1:
                    # get teleport position
                    telloc = get_teleport_location(tiles, [l1[1], l2[1]])
                    # woops..
                    if l1[1][0] + l1[1][1] < l2[1][0] + l2[1][1]:
                        first = l1[0]
                        second = l2[0]
                    else:
                        first = l2[0]
                        second = l1[0]
                    couples.append(((first, second), telloc))
                    break
    start = (0, 0)
    end = (0, 0)
    couples = list(dict.fromkeys(couples))
    temptel = defaultdict(set)
    for c in couples:
        if c[0] == ("A", "A"):
                start = c[1]
        elif c[0] == ("Z", "Z"):
                end = c[1]
        else:
            temptel[c[0]].add(c[1])
    teleports = [[], [], []]
    for t in temptel:
        tup = tuple(temptel[t])
        print (tup)
        teleports[0].append(tup[0])
        teleports[1].append(tup[1])
        teleports[2].append(t)
    return start, end, teleports


def part1(tiles, start, end, teleports,depth=0):
    visited = set()
    visited.add(start)
    while depth == 0 or len(neighbours) > 0:
        neighbours = set()
        for v in visited:
            x, y = v
            directions = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            for d in directions:
                if d in tiles:
                    if d not in visited:
                        neighbours.add(d)
            if tiles[v] == "*":
                telexit = get_teleport_exit(v, teleports)
                if telexit not in visited:
                    neighbours.add(telexit)

        for n in neighbours:
            if n == end:
                return depth + 1
            visited.add(n)
        depth += 1
    return -1


def part2(tiles, start, end, teleports, z=0, depth=0):
    # just BFS copy of 1 with level/z, slow as hell again :D
    if start == end and z==0:
        return depth
    visited = set()
    visited.add((start, z))
    while depth == 0 or len(neighbours) > 0:
        neighbours = set()
        for v in visited:
            x, y = v[0]
            directions = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            for d in directions:
                if d in tiles:
                    test = (d, v[1])
                    if test not in visited:
                        neighbours.add(test)
            if tiles[v[0]] == "*":
                valid = False
                outer = in_outer(v[0])
                if not outer or v[1] is not 0:
                    valid = True
                if valid:
                    if outer:
                        level = v[1]-1
                    else:
                        level = v[1]+1
                    telexit = get_teleport_exit(v[0], teleports)
                    if (telexit, level) not in visited:
                        neighbours.add((telexit, level))
                        print("Levelling {}, depth {}, size visited {}".format(level, depth, len(visited)))
        for n in neighbours:
            if n == (end, 0):
                return depth + 1
            # speedup? level 30 is deep enough
            # if n[1] < 30:
            #     visited.add(n)
            visited.add(n)

        depth += 1
    return -1


def main():
    global WIDTH
    global HEIGHT
    with open("day20.txt", "r") as f:
        data = f.read().split("\n")
    tiles = {}
    HEIGHT = len(data)
    WIDTH = len(data[HEIGHT // 2]) + 2

    letters = []
    for j, row in enumerate(data):
        for i, item in enumerate(row):
            if item not in " #" and not item.isalpha():
                tiles[(i, j)] = item
            if item.isalpha():
                letters.append((item, (i, j)))
    start, end, teleports = make_pairs(tiles, letters)
    tiles[start] = "["
    tiles[end] = "]"
    for l in teleports:
        for index in l:
            tiles[index] = "*"

    print(part1(tiles, start, end, teleports))
    print(part2(tiles, start, end, teleports))

if __name__ == "__main__":
    main()
