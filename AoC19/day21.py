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
            if len(inp):
                data[arg1] = inp.pop(0)
                counter += 2
                continue
            # if provided:
            #     data[arg1] = inp
            #     counter += 2
            #     continue
            else:
                return diag, counter, rbase, True
        elif opcode == 4:
            diag.append(data[arg1])
            counter += 2
            if len(diag) == 1:
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


def run(instructions, data):
    gimme = False
    counter, rbase = 0, 0
    last_output = ""
    while True:
        output, counter, rbase, gimme = solve(data, instructions, counter, rbase, gimme)
        if not output:
            gimme = True
        else:
            try:
                output = chr(output[0])
                print(output, end="")
                if "cc" in output + last_output:
                    print("STOPPPING")
                    break
                last_output = output
            except:
                print(output)
                break


def main():
    with open("day21.txt", "r") as f:
        data = f.read().split(",")
    data = [int(x) for x in data]
    data = data + [0] * 10000

    #part1
    instruction = "NOT C J\nNOT A T\nOR T J\nAND D J\nWALK\n"
    instruction = [ord(char) for char in instruction]
    run(instruction, copy.deepcopy(data))
    #part2
    instruction = "NOT C J\nAND D J \nAND H J\nNOT A T\nAND D T\nOR T J\nNOT B T\nAND D T\nOR T J\nRUN\n"
    instruction = [ord(char) for char in instruction]
    run(instruction, data)


if __name__ == "__main__":
    main()
