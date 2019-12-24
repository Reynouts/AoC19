from collections import deque


class SpaceCards():
    def __init__(self, size):
        self.deck = self.create_deck(size)

    def create_deck(self, size):
        return deque(range(size))

    def new_stack(self):
        self.deck.reverse()

    def cut(self, n):
        self.deck.rotate(n*-1)

    def deal(self, n):
        temp = deque(len(self.deck)*[0])
        index = 0
        for card in self.deck:
            temp[index] = card
            index = (index+n) % len(self.deck)
        self.deck = temp


def shuffle_up_and_deal(data, size, the_one):
    spacecards = SpaceCards(size)
    for line in data:
        if "deal with increment" in line:
            spacecards.deal(int(line.split(" ")[-1]))
        elif "cut" in line:
            spacecards.cut(int(line.split(" ")[-1]))
        elif "new" in line:
            spacecards.new_stack()
    return spacecards.deck.index(the_one)


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


# Iterative Python 3 program to find
# modular inverse using extended
# Euclid algorithm

# Returns modulo inverse of a with
# respect to m using extended Euclid
# Algorithm Assumption: a and m are
# coprimes, i.e., gcd(a, m) = 1
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


def inverted(data, size, index):
    for line in data[::-1]:
        if "deal with increment" in line:
            #index = (int(line.split(" ")[-1]) * index) % size
            # x = (y * z) % p
            # z = (x / % p) * y
            # index = (index / % size) * increment
            # index = pow(size, int(line.split(" ")[-1]), index)
            # Stuck!!
            t = int(line.split(" ")[-1])
            # index = modInverse(t, size) * index
            # index = modInverse(t, index) / size
            # index = modInverse(size, t) / index
            # index = modInverse(size, index) / t
            # index = modInverse(index, size) * t
            # index = modInverse(index, t) / size

            continue
        elif "cut" in line:
            index = (index + int(line.split(" ")[-1])) % size
        elif "new" in line:
            index = (-1 - index) % size
    return index


def main():
    with open("day22.txt", "r") as f:
        data = f.read().split("\n")



    size = 10007
    the_one = 2019
    print("Part 1: {}".format(shuffle_up_and_deal(data, size, the_one)))
    print("Part 1: {}".format(make_it_quick(data, size, the_one)))
    print("Part T: {}".format(inverted(data, size, the_one)))

    # back to original possible (cycle!)
    for i in range(size-1):
        the_one = make_it_quick(data, size, the_one)
    assert the_one == 2019


    size = 119315717514047      #119315717514047
    repeat = 101741582076661    #101741582076661
    the_one = 2020

    shuffles_needed = size-1-repeat
    print(shuffles_needed)
    # too much
    #   - Maybe instructions could be bundles/simplified less overhead
    #   - Do something else with cycles
    #   - Invert the instructions?


if __name__ == "__main__":
    main()
