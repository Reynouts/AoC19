import aocutils as util
from itertools import combinations
import operator
import functools


def solve(data, length, result=2020):
    for x in combinations(data, length):
        if sum(x) == result:
            return functools.reduce(operator.mul, x)


def main():
    day=int(util.os.path.basename(__file__).split(".")[0].split("day")[1])
    data = util.get_file(day)
    data = [int(x) for x in data]
    print("Part 1: {}".format(solve(data, 2)))
    print("Part 2: {}".format(solve(data, 3)))


if __name__ == "__main__":
    main()
