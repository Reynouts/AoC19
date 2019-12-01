import aocutils as util


def tests():
    # Testcases from AoC puzzle example, expanded with own tests
    testcases = []
    for case in testcases:
        assert solve(case[0]) == case[1], "Expected {}, but got {}".format(case[1],solve(case[0]))


def solve():
    return 0


def main():
    tests()
    data = util.get_input(2)
    data = [int(x) for x in data]
    print("Answer {}".format(solve(data)))


if __name__ == "__main__":
    main()