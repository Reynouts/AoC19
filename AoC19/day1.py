import aocutils as util


def tests():
    testcases = []
    testcases.append(([1969], 966))
    testcases.append(([14], 2))
    testcases.append(([100756], 50346))
    testcases.append(([y for x in (x[0] for x in testcases) for y in x], sum(x[1] for x in testcases)))

    for case in testcases:
        assert solve(case[0]) == case[1], "Expected {}, but got {}".format(case[1],solve(case[0]))


def solve(data):
    total = 0
    while len(data) > 0:
        data = [i for i in (x // 3 - 2 for x in data) if i > 0]
        total += sum(data)
    return total


def main():
    tests()
    data = [int(x) for x in util.get_input(1)]
    print("Total fuel needed {}".format(solve(data)))


if __name__ == "__main__":
    main()
