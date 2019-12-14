import aocutils as util
import copy
import os
import time

n=0

def calculate_input(ball, paddle):
    try:
        if ball[0][0] > paddle[0][0]:
            return 1
        elif ball[0][0] < paddle[0][0]:
            return -1
        else:
            return 0
    except:
        return 1


def draw(tiles):
    global n
    result = ""
    locations = tiles.keys()
    for i in range(min(locations)[1], max(locations)[1]+1):
        for j in range (min(locations)[0],max(locations)[0]+1):
            if (j,i) in tiles.keys():
                v = tiles[j,i]
                color = " "
                if v == 0:
                    #if x == "0" else '\033[107m \033[0m'
                    #color = '\033[40m \033[0m'
                    color = " "
                elif v == 1:
                    color = "+"
                    color = u"\u2588"
                elif v == 2:
                    color = u"\u25EB"
                elif v == 3:
                    color = "="
                elif v == 4:
                    #color = chr(169)
                    color = u"\u2092"
                result += color
            else:
                result += " "
        result += "\n"
    time.sleep(0.05)
    cls(n)
    n = display(result[:-1])
    row_count = 20
    rows_full = row_count + 2
    print("\033[F" * rows_full)


def solve(data, inp, counter=0, rbase=0, provided=False):
    current = 0
    diag = []

    while counter < len(data):
        current = data[counter]
        opcode = current % 100
        modes = [int(x) for x in f"{current:05}"[:3][::-1]]

        # Stop the loop when 99 found
        if opcode == 99:
            diag.append(99)
            return diag, counter, rbase, False

        # set index of arg1 corresponding to it's mode
        if modes[0] == 0:
            arg1 = data[counter + 1]
        elif modes[0] == 1:
            arg1 = counter + 1
        else:
            arg1 = data[counter + 1] + rbase

        # opcodes with only first argument
        if opcode == 3:
            if provided:
                data[arg1] = inp
                counter += 2
                continue
            else:
                return diag, counter, rbase, True
        elif opcode == 4:
            diag.append(data[arg1])
            counter += 2
            if len(diag) == 3:
                return diag, counter, rbase, False
            continue
        elif opcode == 9:
            rbase += data[arg1]
            counter += 2
            continue

        # set index of arg2 corresponding to it's mode
        if modes[1] == 0:
            arg2 = data[counter + 2]
        elif modes[1] == 1:
            arg2 = counter + 2
        else:
            arg2 = data[counter + 2] + rbase

        # set index of out parameter corresponding to it's mode
        if modes[2] == 0:
            out = data[counter + 3]
        elif modes[2] == 1:
            out = counter + 3
        else:
            out = data[counter + 3] + rbase

        # opcode handling with multiple arguments
        if opcode == 1:
            data[out] = data[arg1] + data[arg2]
            counter += 4
        elif opcode == 2:
            data[out] = data[arg1] * data[arg2]
            counter += 4
        elif opcode == 5:
            counter = data[arg2] if data[arg1] else counter + 3
        elif opcode == 6:
            counter = data[arg2] if not data[arg1] else counter + 3
        elif opcode == 7:
            data[out] = 1 if data[arg1] < data[arg2] else 0
            counter += 4
        elif opcode == 8:
            data[out] = 1 if data[arg1] == data[arg2] else 0
            counter += 4

    # return last diagnostic code array as output
    return (diag or [None]), counter, rbase, False


def cls(n = 0):
    if n == 0:
        os.system('cls')
    else:
        print('\b'*(n+10))


def display(s):
    #s = '\n'.join(''.join(row) for row in chars)
    print(s)
    return len(s)

def main():
    with open("day13.txt", "r") as f: data = f.read().split(",")
    #data = util.get_input(13, ",")
    data = [int(x) for x in data]
    data = data + [0] * 10000
    odata = copy.deepcopy(data)

    output = [0]
    empty, walls, blocks, paddle, ball = [], [], [], [], []
    counter, rbase = 0, 0
    while True:
        output, counter, rbase, gimme = solve(data, 0, counter, rbase)
        if 99 in output:
            break
        else:
            if output[2] == 0:
                empty.append(output)
            elif output[2] == 1:
                walls.append(output)
            elif output[2] == 2:
                blocks.append(output)
            elif output[2] == 3:
                paddle.append(output)
            elif output[2] == 4:
                ball.append(output)
    print (len(blocks))

    inp = 1
    odata[0] = 2
    counter = 0
    rbase = 0
    blocks, paddle, ball = [], [], []
    tiles = {}
    while True:
        output, counter, rbase, gimme = solve(odata, inp, counter, rbase, gimme)
        if 99 in output:
            break
        else:
            if gimme:
                draw(tiles)
                inp = calculate_input(ball, paddle)
                paddle.clear()
                ball.clear()
            #elif output[0] == -1 and output[1] == 0:
                #print("Score: {}".format(output[2]))

            # elif output[2] == 0:
            #     #empty
            # elif output[2] == 1:
            #     #wall
            # elif output[2] == 2:
            #     blocks.append(output)
            elif output[2] == 3:
                paddle.append(output)
            elif output[2] == 4:
                ball.append(output)
            if len(output) == 3:
                tiles[tuple(output[:2])] = output[2]





if __name__ == "__main__":
    main()
