import aocutils as util
from collections import defaultdict
from math import ceil


def calculate_cost(need, quant, cost, remainder=None):
    if need == "ORE":
        return quant
    elif quant <= remainder[need]:
        remainder[need] -= quant
        return 0
    else:
        quant -= remainder[need]
        remainder[need] = 0
        total = 0
        _quant, _need = cost[need]
        n = ceil(quant / _quant)
        for n_in, e in _need:
            #print ("calculating cost of {}:".format(e))
            n_in *= n
            total += calculate_cost(e, n_in, cost, remainder)
        remainder[need] += _quant * n - quant
        return total


def main():
    with open("day14.txt", "r") as f: data = f.read().split("\n")
    cost = {}
    for d in data:
        inp, outp = d.split(" => ")
        inp = inp.split(", ")
        outp = outp.split(" ")
        outp[0] = int(outp[0])
        cost[outp[1]] = []
        cost[outp[1]].append(outp[0])
        inputs = []
        for i in inp:
            i = i.split(" ")
            i[0] = int(i[0])
            inputs.append((i[0],i[1]))
        cost[outp[1]].append(inputs)
    part1 = calculate_cost("FUEL", 1, cost, defaultdict(int))
    print ("Part 1: {}".format(part1))

    # crappy binary search..
    ore = 1000000000000
    min = 0
    max = 10**100
    diff = 1
    _diff = 0
    while _diff != diff:
        mid = (min+max)//2
        _cost = calculate_cost("FUEL", mid, cost, defaultdict(int))
        _diff = diff
        diff = ore - _cost
        if diff > 0:
            min = mid
        elif diff < 0:
            max = mid
    print("Part 2: {}".format(mid))


if __name__ == "__main__":
    main()
