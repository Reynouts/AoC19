import aocutils as util


class Node:
    def __init__(self, name):
        self.name = name
        self.orbits_around = []
        self.center_of = []
        self.total = -1

    def add_orbits_around(self, node):
        self.orbits_around.append(node)

    def add_center_of(self, node):
        self.center_of.append(node)

    def get_orbits_around(self):
        if self.orbits_around:
            return self.orbits_around[0]
        return

    def get_center_of(self):
        return self.center_of

    def get_neighbours(self):
        return [x for x in [self.get_orbits_around()] + self.get_center_of() if x is not None]

    def get_orbits(self):
        if self.total < 0:
            total = len(self.orbits_around)
            for n in self.orbits_around:
                total += n.get_orbits()
            self.total = total
        return self.total


def bfs(start, end, nodes):
    queue = [start]
    depth = {start: 0}
    visited = []

    while queue:
        current = queue.pop()
        visited.append(current)
        for neighbour in current.get_neighbours():
            if neighbour == end:
                return depth[current] + 1
            if neighbour not in visited:
                queue.append(neighbour)
                depth[neighbour] = depth[current] + 1


def solve(data):
    flattened = [val for sublist in data for val in sublist]
    nodes = {}
    for n in set(flattened):
        nodes[n] = Node(n)
    for edges in data:
        nodes[edges[1]].add_orbits_around(nodes[edges[0]])
        nodes[edges[0]].add_center_of(nodes[edges[1]])
    total = 0
    for item in nodes.items():
        total += item[1].get_orbits()
    print("Part 1: {}".format(total))

    start = nodes["YOU"].get_orbits_around()
    end = nodes["SAN"].get_orbits_around()
    print('Part 2: {}'.format(bfs(start, end, nodes)))


def main():
    data = util.get_input(6)
    data = [x.split(")") for x in data]
    solve(data)


if __name__ == "__main__":
    main()
