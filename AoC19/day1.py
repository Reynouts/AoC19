import aocutils as util


def tests():
    # Testcases from AoC puzzle example, expanded with own tests
    testcases = []
    testcases.append(([1969], 966))
    testcases.append(([14], 2))
    testcases.append(([100756], 50346))
    testcases.append(([y for x in (x[0] for x in testcases) for y in x], sum(x[1] for x in testcases)))
    for case in testcases:
        assert solve(case[0]) == case[1], "Expected {}, but got {}".format(case[1],solve(case[0]))


def solve(data):
    # Actual code for the puzzle. Going "horizontally" through the modules and needed fuel
    total = 0
    while len(data) > 0:
        data = [i for i in (x // 3 - 2 for x in data) if i > 0]
        total += sum(data)
    return total


def main():
    # Get data from day1, after running the testcases
    tests()
    data = util.get_input(1)
    data = [int(x) for x in data]
    print("Total fuel needed {}".format(solve(data)))


if __name__ == "__main__":
    main()
