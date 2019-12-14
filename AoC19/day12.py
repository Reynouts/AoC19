import aocutils as util
from itertools import combinations
from math import gcd
from functools import reduce


class Moon:
    def __init__(self, x, y, z, dx=0, dy=0, dz=0):
        self.positions = [x, y, z]
        self.velocities = [dx, dy, dz]
        self.initial_positions = [x, y, z]
        self.initial_velocities = [dx, dy, dz]

    def apply_gravity(self, other):
        for i, _ in enumerate(self.positions):
            if not self.positions[i] == other.positions[i]:
                if self.positions[i] > other.positions[i]:
                    self.velocities[i] -= 1
                else:
                    self.velocities[i] += 1

    def apply_velocity(self):
        for i, _ in enumerate(self.velocities):
            self.positions[i] += self.velocities[i]

    def p_energy(self):
        return sum([abs(x) for x in self.positions])

    def k_energy(self):
        return sum([abs(x) for x in self.velocities])

    def total_energy(self):
        return self.p_energy() * self.k_energy()

    def repeated_axes(self, axes):
        return self.initial_positions[axes] == self.positions[axes] \
               and self.initial_velocities[axes] == self.velocities[axes]

    def __repr__(self):
        return "pos=<x={:>3}, y={:>3}, z={:>3}>, vel=<x={:>3}, y={:>3}, z={:>3}>".format \
            (self.positions[0], self.positions[1], self.positions[2],
             self.velocities[0], self.velocities[1], self.velocities[2])


def cycle(moons):
    combos = combinations(moons, 2)
    for c in combos:
        c[0].apply_gravity(c[1])
        c[1].apply_gravity(c[0])
    for m in moons:
        m.apply_velocity()


def solve(moons, iterations):
    for _ in range(iterations):
        cycle(moons)
    energy = 0
    for m in moons:
        energy += m.total_energy()
    return energy


def solve_two(moons):
    iterations = 0
    found = [0, 0, 0]
    while not all(found):
        cycle(moons)
        iterations += 1
        for i in range(3):
            if found[i] == 0:
                r = []
                for m in moons:
                    r.append(m.repeated_axes(i))
                if all(r):
                    found[i] = iterations
    return reduce(lambda a, b: a * b // gcd(a, b), found)


def preprocess(data):
    moons = []
    for line in data:
        moons.append(Moon(*[int(x.split("=")[1]) for x in line[1:-1].split(", ")]))
    return moons


def main():
    # testcases
    data = ["<x=-1, y=0, z=2>", "<x=2, y=-10, z=-7>", "<x=4, y=-8, z=8>", "<x=3, y=5, z=-1>"]
    assert (solve(preprocess(data), 10) == 179)
    assert (solve_two(preprocess(data)) == 2772)
    data = ["<x=-8, y=-10, z=0>", "<x=5, y=5, z=10>", "<x=2, y=-7, z=3>", "<x=9, y=-8, z=-3>"]
    assert (solve_two(preprocess(data)) == 4686774924)

    # puzzle input from server
    data = util.get_input(12, "\n")
    print("Part 1: {}".format(solve(preprocess(data), 1000)))
    print("Part 2: {}".format(solve_two(preprocess(data))))


if __name__ == "__main__":
    main()
