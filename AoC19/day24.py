import copy
import aocutils as util


def grid_to_string(tiles, linebreak=False, z=0):
    result = ""
    for j in range(5):
        for i in range(5):
            if (z, i, j) in tiles:
                result += tiles[z, i, j]
            else:
                result += " "
        if linebreak:
            result += "\n"
    return result


def evolve(tiles, part2=True):
    _tiles = {}
    for t in tiles:
        sur = 0
        z, x, y = t
        if (x, y) == (2, 2) and part2:
            continue
        directions = [(z, x - 1, y), (z, x + 1, y), (z, x, y - 1), (z, x, y + 1)]
        for d in directions:
            if d in tiles:
                if tiles[d] == "#":
                    sur += 1
            # if t at edge, check outer grid neighbours
            combi = {(1, -1): (d[0]+1, 1, 2), (1, 5): (d[0]+1, 3, 2), (2, -1): (d[0]+1, 2, 1), (2, 5): (d[0]+1, 2, 3)}
            for c in combi:
                if d[c[0]] == c[1]:
                    if combi[c] in tiles:
                        if tiles[combi[c]] == "#":
                            sur += 1
                    break
            # check middle, down a level
            if d[1] == 2 and d[2] == 2:
                combi = {(2,1): 0, (1,2): 0, (2,3):  4, (3,2): 4}
                for c in combi:
                    if (x, y) == c:
                        for p in range(5):
                            check = (z - 1, p, combi[c]) if x == 2 else (z-1, combi[c], p)
                            if check in tiles:
                                if tiles[check] == "#":
                                    sur += 1
        if tiles[t] == "#":
            _tiles[t] = "#" if sur == 1 else "."
        else:
            _tiles[t] = "#" if sur == 1 or sur == 2 else tiles[t]
    return _tiles


def bio_rating(state):
    rating = 0
    for i, s in enumerate(state):
        if s == "#":
            rating += 2 ** i
    return rating


def expand_tiles(tiles, level):
    level += 1
    for y in range(5):
        for x in range(5):
            tiles[level, x, y] = "."
            tiles[level * -1, x, y] = "."
    return tiles, level


@util.timeit
def main():
    with open("day24.txt", "r") as f:
        data = f.read().split("\n")

    tiles = {}
    for j, row in enumerate(data):
        for i, item in enumerate(row):
            tiles[(0, i, j)] = item

    # part 1
    _tiles = copy.deepcopy(tiles)
    found = ""
    states = []
    while True:
        _tiles = evolve(_tiles, False)
        state = grid_to_string(_tiles)
        if state in states:
            found = state
            break
        else:
            states.append(state)
    print("Part 1: {}".format(bio_rating(state)))

    # part 2
    level = 0
    iterations = 200
    for _ in range(iterations):
        tiles, level = expand_tiles(tiles, level)
        tiles = evolve(tiles)
    print("Part 2: {}".format(sum([1 for x in tiles.values() if x == "#"])))


if __name__ == "__main__":
    main()
