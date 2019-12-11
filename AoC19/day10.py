import aocutils as util
from math import gcd, atan2


def checksight(source, target, astroids):
    distance = (target[0]-source[0], target[1]-source[1])
    denom = gcd(*distance)
    if denom == 1 or denom == 0:
        return target
    else:
        step = [x//denom for x in distance]
        position = source
        while position != target:
            position = tuple(map(sum, zip(position, step)))
            if position == target:
                return target
            elif position in astroids:
                return None
        return target


def solve(data):
    astroids = []
    for j, row in enumerate(data):
        for i, item in enumerate(row):
            if item == "#":
                astroids.append((i,j))

    best = 0
    radar = (0, 0)
    bucky = []
    for a in astroids:
        bucket = []
        for b in astroids:
            if not a == b:
                droid = checksight(a, b, astroids)
                if droid:
                    bucket.append(droid)
        if len(bucket) > len(bucky):
            radar = a
            bucky = bucket
    part1 = len(bucky)

    angles = []
    for astroid in bucky:
        dx = astroid[0] - radar[0]
        dy = astroid[1] - radar[1]
        angle = atan2(dx, dy)
        angles.append((angle, astroid, (astroid[1] - radar[1], astroid[0] - radar[0])))
    angles = sorted(angles)[::-1]
    part2 = angles[199][1][0]*100 + angles[199][1][1]

    return part1, part2


def main():
    #testcase
    with open("day10.txt", "r") as f: data = f.read().split("\n")
    p1, p2 = solve(data)
    assert(p1 == 210)
    assert(p2 == 802)

    #data from server
    data = util.get_input(10, "\n")
    p1, p2 = solve(data)
    print ("Part 1: {}\nPart 2: {}".format(p1, p2))


if __name__ == "__main__":
    main()
