import aocutils as util
import copy
import itertools


def solve(data, input, first, counter=0):
    current = 0
    if counter == 0:
        boot = True
    else:
        boot = False
    diag = []
    while counter < len(data):
        current = data[counter]
        opcode = current % 100
        modes = [int(x) for x in f"{current:04}"[:2][::-1]]

        if opcode == 99:
            break
        elif current == 3:
            if boot:
                data[data[counter + 1]] = first
                boot = False
            else:
                data[data[counter + 1]] = input
            counter += 2
            continue
        elif opcode == 4:
            diag.append(data[data[counter + 1]])
            return data[data[counter + 1]], counter+2

        arg1 = data[data[counter + 1]] if modes[0] == 0 else data[counter + 1]
        arg2 = data[data[counter + 2]] if modes[1] == 0 else data[counter + 2]
        if opcode == 1:
            data[data[counter + 3]] = arg1 + arg2
            counter += 4
        elif opcode == 2:
            data[data[counter + 3]] = arg1 * arg2
            counter += 4
        elif opcode == 5:
            counter = arg2 if arg1 else counter + 3
        elif opcode == 6:
            counter = arg2 if not arg1 else counter + 3
        elif opcode == 7:
            data[data[counter + 3]] = 1 if arg1 < arg2 else 0
            counter += 4
        elif opcode == 8:
            data[data[counter + 3]] = 1 if arg1 == arg2 else 0
            counter += 4
    return (diag or [None])[-1], counter


def run(looping, data, phases):
    result = 0
    for test in phases:
        ampdata = []
        input = 0
        for t in test:
            d = copy.deepcopy(data)
            input, pointer = solve(data, input, t)
            ampdata.append([d, pointer])
        running = True
        while running and looping:
            for i, g in enumerate(ampdata):
                input, pointer = solve(g[0], input, input, g[1])
                if not input:
                    running = False
                    input = float('-inf')
                    break
                ampdata[i] = [g[0], pointer]
            if input > result:
                result = input
        if input > result:
            result = input
    return result


def main():
    data = util.get_input(7, ",")
    data = [int(x) for x in data]
    print("Part 1: {}".format(run(False, data, list(itertools.permutations([0, 1, 2, 3, 4])))))
    print("Part 2: {}".format(run(True, data, list(itertools.permutations([5, 6, 7, 8, 9])))))


if __name__ == "__main__":
    main()
