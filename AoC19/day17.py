import copy


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
                d[(x,y)] = item
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
    inp = []
    gimme = False
    counter, rbase = 0, 0
    while True:
        output, counter, rbase, gimme = solve(data, inp, counter, rbase, gimme)
        if not output:
            gimme = True
            if instructions:
                inp = instructions.pop(0)
        else:
            try:
                output = chr(output[0])
                #print(output, end="")
            except:
                return (output[0])



def part1(data):
    gimme = True
    inp, counter, rbase = 1, 0, 0
    current = (0, 0)
    heading = {1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1), }
    tiles = []
    last_move = inp
    cycles = 0
    goal = ()
    while True:
        output, counter, rbase, gimme = solve(data, inp, counter, rbase, gimme)
        if 99 in output:
            break
        else:
            tiles.append(output[0])
    grid = stringtogrid(tiles)
    points = gridtodict(grid)

    result = 0
    for i in points.keys():
        if checkpoint(points, i):
            result += (i[0]*i[1])
    return result


def main():
    with open("day17.txt", "r") as f:
        data = f.read().split(",")
    data = [int(x) for x in data]
    data = data + [0] * 10000

    print("Part 1: {}".format(part1(copy.deepcopy(data))))

    # FULL: L,12,R,8,L,6,R,8,L,6,R,8,L,12,L,12,R,8,L,12,R,8,L,6,R,8,L,6,L,12,R,8,L,6,R,8,L,6,R,8,L,12,L,12,R,8,L,6,R,6,L,12,R,8,L,12,L,12,R,8,L,6,R,6,L,12,L,6,R,6,L,12,R,8,L,12,L,12,R,8
    # MAIN: A,B,A,A,B,C,B,C,C,B
    # A:    L,12,R,8,L,6,R,8,L,6
    # B:    R,8,L,12,L,12,R,8
    # C:    L,6,R,6,L,12

    data[0] = 2
    main = [ord(char) for char in "A,B,A,A,B,C,B,C,C,B\n"]
    A = [ord(char) for char in "L,12,R,8,L,6,R,8,L,6\n"]
    B = [ord(char) for char in "R,8,L,12,L,12,R,8\n"]
    C = [ord(char) for char in "L,6,R,6,L,12\n"]
    answer = [ord(char) for char in "N\n"]
    instructions = [main, A, B, C, answer]
    print("Part 2: {}".format(run(instructions, data)))
    

if __name__ == "__main__":
    main()
