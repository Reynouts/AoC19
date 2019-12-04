import aocutils as util


def solve(data):
    paths = []
    for path in data:
        paths.append({})
        current = (0, 0)
        dxy = (0, 0)
        totalsteps = 0
        for instruction in path:
            heading, steps = instruction[0], int(instruction[1:])
            if heading == "R":
                dxy = (1,0)
            elif heading == "L":
                dxy = (-1,0)
            elif heading == "U":
                dxy = (0,-1)
            elif heading == "D":
                dxy = (0,1)
            for i in range(steps):
                current = tuple(sum(i) for i in zip(current, dxy))
                paths[-1][current] = totalsteps + i + 1
            totalsteps += steps
    intersection = list(set(paths[0].keys()) & set(paths[1].keys()))
    manhattan = 10**100
    delay = 10**100
    for i in intersection:
        cmanhattan = abs(i[0]) + abs(i[1])
        cdelay = paths[0][i] + paths [1][i]
        if cmanhattan <= manhattan:
            manhattan = cmanhattan
        if cdelay <= delay:
            delay = cdelay
    print ("Part 1: {}".format(manhattan))
    print ("Part 2: {}".format(delay))


def main():
    data = [x.split(',') for x in util.get_input(3)]
    solve(data)


if __name__ == "__main__":
    main()