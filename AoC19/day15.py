import aocutils as util
import copy
import os
import time
from random import randint
import msvcrt



def calculate_input(tiles, last_move):
    if last_move[1][0] == 0:
        move = randint(1, 4)
        while move == last_move[0]:
            move = randint(1, 4)
        return move
    else:
        return randint(1, 4)


def draw(tiles, current, end=False):
    result = "========================================================\n"
    locations = tiles.keys()
    for j in range(-20, 20):
        for i in range(-31, 31):
            if (j, i) in tiles.keys():
                v = tiles[j, i]
                color = " "
                if (j, i) == (0, 0):
                    color = "S"
                elif (j, i) == current:
                    if end:
                        color = "E"
                    else:
                        color = "D"
                elif v == 0:
                    color = "#"
                elif v == 1:
                    color = " "
                elif v == 2:
                    color = "+"
                result += color
            else:
                result += "."
        result += "\n"
    result += "\n"
    time.sleep(0.1)
    os.system("cls")
    print(result)


def solve(data, inp, counter=0, rbase=0, provided=False):
    current = 0
    diag = []

    while counter < len(data):
        current = data[counter]
        opcode = current % 100
        modes = [int(x) for x in f"{current:05}"[:3][::-1]]

        # Stop the loop when 99 found
        if opcode == 99:
            diag.append(99)
            return diag, counter, rbase, False

        # set index of arg1 corresponding to it's mode
        if modes[0] == 0:
            arg1 = data[counter + 1]
        elif modes[0] == 1:
            arg1 = counter + 1
        else:
            arg1 = data[counter + 1] + rbase

        # opcodes with only first argument
        if opcode == 3:
            if provided:
                data[arg1] = inp
                counter += 2
                continue
            else:
                return diag, counter, rbase, True
        elif opcode == 4:
            diag.append(data[arg1])
            counter += 2
            if len(diag) == 1:
                return diag, counter, rbase, False
            continue
        elif opcode == 9:
            rbase += data[arg1]
            counter += 2
            continue

        # set index of arg2 corresponding to it's mode
        if modes[1] == 0:
            arg2 = data[counter + 2]
        elif modes[1] == 1:
            arg2 = counter + 2
        else:
            arg2 = data[counter + 2] + rbase

        # set index of out parameter corresponding to it's mode
        if modes[2] == 0:
            out = data[counter + 3]
        elif modes[2] == 1:
            out = counter + 3
        else:
            out = data[counter + 3] + rbase

        # opcode handling with multiple arguments
        if opcode == 1:
            data[out] = data[arg1] + data[arg2]
            counter += 4
        elif opcode == 2:
            data[out] = data[arg1] * data[arg2]
            counter += 4
        elif opcode == 5:
            counter = data[arg2] if data[arg1] else counter + 3
        elif opcode == 6:
            counter = data[arg2] if not data[arg1] else counter + 3
        elif opcode == 7:
            data[out] = 1 if data[arg1] < data[arg2] else 0
            counter += 4
        elif opcode == 8:
            data[out] = 1 if data[arg1] == data[arg2] else 0
            counter += 4

    # return last diagnostic code array as output
    return (diag or [None]), counter, rbase, False


def floodfill(tiles, start, depth=0):
    visited = set()
    visited.add(start)

    while depth == 0 or len(neighbours) > 0:
        neighbours = set()
        for v in visited:
            x, y = v
            directions = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            for d in directions:
                if d in tiles.keys():
                    if d not in visited:
                        if tiles[d] > 0:
                            neighbours.add(d)
        for n in neighbours:
            visited.add(n)
        depth += 1
    return depth - 1


def get_manual_input():
    i = msvcrt.getch()
    output = {b"w": 1, b"s": 2, b"a": 3, b"d": 4}
    return output[i]


def main():
    with open("day15.txt", "r") as f:
        data = f.read().split(",")
    data = [int(x) for x in data]
    data = data + [0] * 10000

    gimme = True
    inp, counter, rbase = 1, 0, 0
    current = (0, 0)
    heading = {1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1), }
    tiles = {current: 1}
    last_move = inp
    cycles = 0
    goal = ()
    while True:
        output, counter, rbase, gimme = solve(data, inp, counter, rbase, gimme)
        last_move = (inp, output)
        _o, counter, rbase, gimme = solve(data, inp, counter, rbase, gimme)
        if 99 in _o:
            break
        else:
            if len(last_move[1]) == 1:
                checked_location = tuple(map(sum, zip(current, heading[inp])))
                tiles[checked_location] = output[0]
                if output[0] != 0:
                    current = checked_location
                    if output[0] == 2:
                        draw(tiles, current, True)
                        print("EXIT found on: {}".format(current))
                        goal = current
                # to make sure there is enough explored (-20,-20 is domain knowledge after looking at output..)
                if (-20, -20) in tiles.keys() and (14, 14) in tiles.keys():
                    print("OK let's go")
                    break
                cycles += 1
                if cycles % 10000 == 0:
                    draw(tiles, current)
                inp = calculate_input(tiles, last_move)
                # if you like to play yourself:
                #draw(tiles, current)
                #inp = get_manual_input()
    visited = set()
    print(floodfill(tiles, goal))


if __name__ == "__main__":
    main()
