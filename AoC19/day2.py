import aocutils as util
import copy


def solve(data):
    counter = 0
    current = 0
    while counter < len(data):
        current = data[counter]
        if current == 99:
            break
        arg1 = data[data[counter+1]]
        arg2 = data[data[counter+2]]
        out = data[counter+3]
        if current == 1:
            data[out] = arg1 + arg2
        elif current == 2:
            data[out] = arg1 * arg2
        counter += 4
    return data[0]


def main():
    data = util.get_input(2, ",")
    data = [int(x) for x in data]
    print("Result part 1: {}".format(solve(copy.deepcopy(data))))

    expected = 19690720
    for i in range(100):
        for j in range(100):
            cdata = copy.deepcopy(data)
            cdata[1] = i
            cdata[2] = j
            result = solve(cdata)
            if result == expected:
                print("Result part 2: {}".format(100 * i + j))
                return


if __name__ == "__main__":
    main()