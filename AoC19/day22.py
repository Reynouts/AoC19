from collections import deque


def make_it_quick(data, size, the_one):
    for line in data:
        if "deal with increment" in line:
            the_one = (int(line.split(" ")[-1]) * the_one) % size
            # x = (y * z) % p
            # z = (x / % p) * y
        elif "cut" in line:
            the_one = (the_one - int(line.split(" ")[-1])) % size
        elif "new" in line:
            the_one = (-1 - the_one) % size
    return the_one


# https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/
def modInverse(a, m):
    m0 = m
    y = 0
    x = 1

    if (m == 1):
        return 0

    while (a > 1):
        # q is quotient
        q = a // m

        t = m

        # m is remainder now, process
        # same as Euclid's algo
        m = a % m
        a = t
        t = y

        # Update x and y
        y = x - q * y
        x = t

        # Make x positive
    if (x < 0):
        x = x + m0

    return x


def part2(f, s, reps, size, index):
    return pow(f, reps, size) * index + (pow(f, reps, size) - 1) * modInverse(f - 1, size) * s


def main():
    with open("day22.txt", "r") as f:
        data = f.read().split("\n")

    size = 10007
    the_one = 2019
    print("Part 1: {}".format(make_it_quick(data, size, the_one)))

    # back to original possible (cycle!)
    for i in range(size-1):
        the_one = make_it_quick(data, size, the_one)
    assert the_one == 2019

    size = 119315717514047
    repeat = 101741582076661
    the_one = 2020

    #shuffles_needed = size-1-repeat
    #print(shuffles_needed)
    # too much
    #   - Maybe instructions could be bundles/simplified less overhead
    #   - Do something else with cycles
    #   - Invert the instructions?
    #   - OK needed quite some help with this.. math!
    #   - modInverse copied from https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/
    p = make_it_quick(data, size, 0)
    f = modInverse((make_it_quick(data, size, 1) - p) % size, size)
    s = (-f * p) % size
    print("Part 2: {}".format(part2(f, s, repeat, size, the_one) % size))


if __name__ == "__main__":
    main()
