import copy


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
            print ( "00 progble")
            return diag, counter, rbase, True

        # set index of arg1 corresponding to it's mode
        if modes[0] == 0:
            arg1 = data[counter + 1]
        elif modes[0] == 1:
            arg1 = counter + 1
        else:
            arg1 = data[counter + 1] + rbase

        # opcodes with only first argument
        if opcode == 3:
            # if not provided:
            #     return diag, counter, rbase, True
            # if len(inp):
            #     print("conmsuming")
            #     data[arg1] = inp.pop(0)
            # else:
            #     data[arg1] = -1
            # provided = False
            print ("Need a value")
            data[arg1] = yield
            counter += 2
            continue
        elif opcode == 4:
            diag.append(data[arg1])
            #yield data[arg1]
            if len(diag) == 3:
                yield diag[-3:]
                diag = []
            counter += 2
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
    print("WHAT?")
    return (diag or [None]), counter, rbase, False


def run(data):
    computers = []
    for i in range(50):
        computers.append([])
        computers[-1] = [copy.deepcopy(data), [i], 0, 0, True] #data, instructionqueue, counter, rbase, gimme
    while True:
        for i, c in enumerate(computers):
            #print("Computer: {}, length: {} queue: {}".format(i, len(c[1]), c[1]))
            output, c[2], c[3], c[4] = solve(c[0], c[1], c[2], c[3], c[4])
            #print ("Computer: {}, output: {}".format(i, output))
            if len(output) >= 3:
                if output[0] == 255:
                    # first number send to 255
                    return output[0]
                if output[0] < len(computers):
                    print ("appending")
                    computers[output[0]][1].extend(output[1:3]) #add X, Y to instructions of computer
                output = output[3:]
            else:
                #print ("What happened?! {}".format(output))
                if 99 in output:
                    print("ERR: Computer: {}, output: {}".format(i, output))
                    return
    print ("End")


def main():
    with open("day21.txt", "r") as f:
        data = f.read().split(",")
    data = [int(x) for x in data]
    data = data + [0] * 10000

    #print(run(data))

    inp = []
    counter = 0
    rbase = 0
    provided = True
    computers = []
    qs = []
    for i in range(50):
        computers.append(solve(copy.deepcopy(data), inp, counter, rbase, provided))
        qs.append([i])
        computers[-1].send(None)
    while True:
        for i, c in enumerate(computers):
            inp = qs[i][0] if len(qs[i]) > 1 else -1
            print("Sending {}, to computer {}".format(inp, i))
            output = c.send(inp)
            if not output:
                # input send, delete from queue
                if qs[i]:
                    qs[i].pop(0)
            else:
                # get triple input
                target, x, y = output
                if target < len(computers):
                    qs[target].append([x, y])
                elif target == 255:
                    print ("Part 1: {}".format(y))





if __name__ == "__main__":
    main()
