import copy
import aocutils as util

# global memory
points = {}


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
                provided = False
                continue
            else:
                return diag, counter, rbase, True
        elif opcode == 4:
            diag.append(data[arg1])
            counter += 2
            if len(diag) > 0:
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


def check(data, x, y):
    # do some memoization
    global points
    if (x, y) in points:
        return points[(x,y)]
    else:
        data = copy.deepcopy(data)
        counter, rbase = 0, 0
        output, counter, rbase, gimme = solve(data, x, counter, rbase, True)
        output, counter, rbase, gimme = solve(data, y, counter, rbase, True)
        points[(x, y)] = output[-1]
        return output[-1]


@util.timeit
def part1(_data):
    result = 0
    for y in range(50):
        for x in range(50):
            data = copy.deepcopy(_data)
            output = check(copy.deepcopy(data), x, y)
            if output == 1:
                result += 1
    return result


@util.timeit
def part2(data):
    # very slow brute force solution.. (8 minutes), but it works.
    y, x = 0, 0
    start, end = 0, 0
    while True:
        while not check(data, x, y):
            x += 1
        start = x
        if check(data, start + 99, y):
            while check(data, x, y):
                x += 1
            end = x - 1
            if check(data, end, y + 99) and check(data, end - 99, y + 99):
                for search in range(end - 99, start - 1, -1):
                    if not check(data, search, y + 99):
                        print("x,y: {},{}".format(search + 1, y))
                        return (search + 1) * 10000 + y
        y += 1
        x = start


def main():
    with open("day19.txt", "r") as f:
        data = f.read().split(",")
    data = [int(x) for x in data]
    data += [0] * 10000
    print("Part 1: {}".format(part1(data)))
    print("Part 2: {}".format(part2(data)))


if __name__ == "__main__":
    main()
