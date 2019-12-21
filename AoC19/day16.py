import aocutils as util
import copy


def phase(_data, pattern, offset=0):
    for i, _ in enumerate(_data):
        result = 0
        _pattern = []
        for p in pattern:
            _pattern.extend([p] * (i+1))
        for j, _ in enumerate(_data):
            result += _data[j] * _pattern[(j+1) % len(_pattern)]
        _data[i] = int(str(result)[-1])
    return _data


def formula_for_one(data, offset):
    psum = sum(data[offset:])
    for i in range(offset, len(data)):
        _old = data[i]
        #data[i] = int(str(partialsum)[-1])
        data[i] = abs(psum) % 10  # twice as fast as above line for this total case
        psum -= _old


def solve(data, repeats):
    pattern = (0, 1, 0, -1)
    for i in range(repeats):
        phase(data, pattern)
    return "".join(str(x) for x in data)[:8]


def solve_two(data, repeats):
    offset = int(("".join(str(x) for x in data[:7])))
    data *= 10000
    for i in range(repeats):
        formula_for_one(data, offset)
    return "".join(str(x) for x in data)[offset:(offset+8)]


def main():
    data = util.get_input(16, " ")[0]
    data = "80871224585914546619083218645595"
    data = [int(x) for x in data]
    result = solve(data, 100)
    assert "".join(str(x) for x in result)[:8] == "24176176"

    data = "19617804207202209144916044189917"
    data = [int(x) for x in data]
    result = solve(data, 100)
    assert "".join(str(x) for x in result)[:8] == "73745418"

    data = "69317163492948606335995924319873"
    data = [int(x) for x in data]
    result = solve(data, 100)
    assert "".join(str(x) for x in result)[:8] == "52432133"

    data = util.get_input(16, " ")[0]
    data = [int(x) for x in data]
    _data = copy.deepcopy(data) #for part2

    print("Part 1: {}".format(solve(data, 100)))
    print("Part 2: {}".format(solve_two(_data, 100)))


if __name__ == "__main__":
    main()
