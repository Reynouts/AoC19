import copy
import itertools


def checkpoint(dict, position):
    x, y = position
    directions = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    for d in directions:
        if d not in dict.keys():
            return False
    return True


def draw_grid(grid):
    result = ""
    for j in grid:
        for i in j:
            result += i
        result += "\n"
    print(result)


def stringtogrid(s):
    grid = [[]]
    for i in s:
        if chr(i) == "\n":
            grid.append([])
        else:
            grid[-1].append(i)
    return grid


def gridtodict(grid):
    d = {}
    for y, row in enumerate(grid):
        for x, item in enumerate(row):
            if chr(item) in "#^<>v":
                d[(x, y)] = item
    return d


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
            if len(inp):
                data[arg1] = inp.pop(0)
                counter += 2
                continue
            # if provided:
            #     data[arg1] = inp
            #     counter += 2
            #     continue
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


def run(instructions, data):
    written = ["south", "take food ration", "west", "take sand", "north", "north", "east", "take astrolabe", "west",
               "south", "south", "east", "north", "north", "east", "take coin", "west", "south", "east", "take cake",
               "south", "take weather machine", "west", "take ornament", "west", "take jam", "east", "east", "north",
               "east", "east", "east", "south"]
    items = ["food ration", "sand", "astrolabe", "cake", "weather machine", "ornament", "jam", "coin"]
    written.extend(["drop " + x for x in items])
    for i in range(1, len(items) + 1):
        for i in list(itertools.combinations(items, i)):
            for j in i:
                written.append("take "+j)
            written.append("south")
            for j in i:
                written.append("drop "+j)
    inp = []
    gimme = False
    counter, rbase = 0, 0
    instructions = []
    last_char = ""
    sec_last = ""
    while True:
        output, counter, rbase, gimme = solve(data, inp, counter, rbase, gimme)
        if not output:
            gimme = True
            if not instructions:
                if written:
                    instructions = written.pop(0)
                else:
                    instructions = input()
                instructions = [ord(char) for char in instructions]
                instructions.append(10)
                inp = instructions
                instructions = []
        else:
            try:
                output = chr(output[0])
                if sec_last == "c" and last_char == "c" and output == "c":
                    break
                print(output, end="")
                sec_last = last_char
                last_char = output

            except:
                return (output[0])


def main():
    with open("day25.txt", "r") as f:
        data = f.read().split(",")
    data = [int(x) for x in data]
    data = data + [0] * 10000
    run([], data)


if __name__ == "__main__":
    main()
