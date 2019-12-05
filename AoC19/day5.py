import aocutils as util
import copy


def solve(data, input):
    counter = 0
    current = 0
    diag = 0
    while counter < len(data):
        current = data[counter]
        opcode = current % 100
        modes = [int(x) for x in f"{current:04}"[:2][::-1]]

        if opcode == 99:
            break
        elif opcode == 4:
            diag = data[data[counter+1]]
            counter += 2
            continue

        arg1 = data[data[counter + 1]] if modes[0] == 0 else data[counter + 1]
        arg2 = data[data[counter + 2]] if modes[1] == 0 else data[counter + 2]
        if opcode == 1:
            data[data[counter+3]] = arg1 + arg2
            counter += 4
        elif opcode == 2:
            data[data[counter+3]] = arg1 * arg2
            counter += 4
        elif current == 3:
            data[data[counter+1]] = input
            counter +=2
        elif opcode == 5:
            counter = arg2 if arg1 else counter+3
        elif opcode == 6:
            counter = arg2 if not arg1 else counter+3
        elif opcode == 7:
            data[data[counter+3]] = 1 if arg1 < arg2 else 0
            counter += 4
        elif opcode == 8:
            data[data[counter+3]] = 1 if arg1 == arg2 else 0
            counter += 4
    return diag


def main():
    data = util.get_input(5, ",")
    data = [int(x) for x in data]
    print ("Part 1: {}".format(solve(copy.deepcopy(data), 1)))
    print ("Part 2: {}".format(solve(copy.deepcopy(data), 5)))


if __name__ == "__main__":
    main()