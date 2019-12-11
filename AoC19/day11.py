import aocutils as util
import copy


def solve(data, inp, counter=0, rbase=0):
    current = 0
    diag = []

    while counter < len(data):
        current = data[counter]
        opcode = current % 100
        modes = [int(x) for x in f"{current:05}"[:3][::-1]]

        # Stop the loop when 99 found
        if opcode == 99:
            return [99], counter, rbase

        # set index of arg1 corresponding to it's mode
        if modes[0] == 0:
            arg1 = data[counter + 1]
        elif modes[0] == 1:
            arg1 = counter + 1
        else:
            arg1 = data[counter + 1] + rbase

        # opcodes with only first argument
        if opcode == 3:
            data[arg1] = inp
            counter += 2
            continue
        elif opcode == 4:
            diag.append(data[arg1])
            counter += 2
            if len(diag) == 2:
                return diag, counter, rbase
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
    return (diag or [None]), counter, rbase


def paint(data, parttwo=False):
    iterations = 0
    black = set()
    white = set()
    current = (0, 0)
    if parttwo:
        white.add(current)
    heading = 0
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    pointer = 0
    rbase = 0
    while True:
        inp = 1 if current in white else 0
        output, pointer, rbase = solve(data, inp, pointer, rbase)
        if output[0] == 99:
            break
        else:
            if output[0] == 1:
                white.add(current)
                black.discard(current)
            else:
                black.add(current)
                white.discard(current)
            if output[1] == 0:
                # left -1,0 -> 0,-1 -> 1,0 -> 0,1
                heading = (heading + 1) % len(directions)
            elif output[1] == 1:
                heading = heading - 1
                if heading < 0:
                    heading = len(directions)-1
            current = tuple(map(sum, zip(current, directions[heading])))
        iterations += 1
    if not parttwo:
        return len(white) + len(black)
    return white


def main():
    data = util.get_input(11, ",")
    data = [int(x) for x in data]
    data = data + [0] * 10000

    print("Part 1: {}".format(paint(copy.deepcopy(data))))

    on = paint(copy.deepcopy(data), True)
    result = ""
    for i in range(min(on)[0], max(on)[0]+1):
        for j in range (min(on)[1],max(on)[1]+1):
            if (i,j) in on:
                result += "\033[40m  \033[0m"
            else:
                result += "\033[107m  \033[0m"
        result += "\n"
    print ("Part 2:\n{}".format(result))



if __name__ == "__main__":
    main()
