import os
from textwrap import wrap


def matrixprinter(layer):
    encoded = ['\033[40m \033[0m' if x == "0" else '\033[107m \033[0m' for x in layer]
    i = 0
    m = []
    result = ""
    while i < 25 * 6:
        result += ("".join(encoded[i:i + 25])) + "\n"
        m.append(encoded[i:i + 25])
        i = i + 25
    os.system("cls")
    print(result)



def solve(data):
    min = 10 ** 100
    mlayer = None
    for layer in data:
        nzero = layer.count("0")
        if nzero < min:
            mlayer = layer
            min = nzero
    ones = mlayer.count("1")
    twos = mlayer.count("2")
    return ones * twos


def main():
    with open("day8.txt","r") as f: data = f.read()
    width, height = 25, 6
    data = wrap(data, width * height)
    print("Part 1: {}".format(solve(data)))

    encoded = []
    for i in range(150):
        for layer in data:
            #matrixprinter("".join(encoded[0:i])+ layer[i:])
            if not layer[i] == "2":
                encoded.append(layer[i])
                break
    matrixprinter(encoded)


if __name__ == "__main__":
    main()
