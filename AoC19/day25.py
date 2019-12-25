import itertools
import random


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


def parse(story):
    # got this blacklist by looking at the output, but could have been automated
    blacklist = ["infinite loop", "photons", "molten lava", "giant electromagnet", "escape pod"]
    actions = []
    movement = []
    if "here lead:" in story:
        d = story.split("here lead:")[-1]
        directions = ("north", "south", "east", "west")
        for direction in directions:
            if direction in d:
                movement.append(direction)
    if "Items" in story:
        items = story.split("Items here:")[1]
        items = items.split("\nCommand?\n")
        items = items[0].split("- ")[1::]
        for x in items:
            item = x[:-1]
            if item not in blacklist:
                actions.append("take " + x[:-1])
    return actions, movement


def get_items(story):
    inventory = []
    if "Items" in story:
        items = story.split("Items in your inventory:")[1]
        items = items.split("\nCommand?\n")
        items = items[0].split("- ")[1::]
        for x in items:
            inventory.append(x[:-1])
    return inventory


def run(instructions, data, console=True, manual=False, max_steps=250):
    gimme, endgame, inv = False, False, False
    counter, rbase, steps = 0, 0, 0
    instructions, buffer, actions, movement, written, inp = [], [], [], [], [], []
    last_char, sec_last = "", ""
    while True:
        output, counter, rbase, gimme = solve(data, inp, counter, rbase, gimme)
        if not output:
            gimme = True
            story = ''.join(buffer)
            if steps > max_steps and "Security" in story:
                endgame = True
            elif "==" in story:
                actions, movement = parse(story)
            if not instructions:
                if endgame and not manual:
                    if written:
                        instructions = written.pop(0)
                    elif inv:
                        items = get_items(story)
                        written.extend(["drop " + x for x in items])
                        for i in range(1, len(items) + 1):
                            for i in list(itertools.combinations(items, i)):
                                for j in i:
                                    written.append("take " + j)
                                written.append("south")
                                for j in i:
                                    written.append("drop " + j)
                        instructions = written.pop(0)
                    else:
                        instructions = "inv"
                        inv = True
                else:
                    if manual:
                        instructions = input()
                    elif actions:
                        # favor actions/taking items over moving
                        instructions = random.choice(actions)
                        actions.remove(instructions)
                    else:
                        instructions = random.choice(movement)
                        actions = []
                        movement = []
                        steps += 1
                if console and not manual:
                    print(instructions)
                instructions = [ord(char) for char in instructions]
                instructions.append(10)
                inp = instructions
                instructions = []
                buffer = []
        else:
            output = chr(output[0])
            if sec_last == "c" and last_char == "c" and output == "c":
                story = ''.join(buffer)
                return [int(s) for s in story.split() if s.isdigit()][-1]
            sec_last = last_char
            last_char = output
            buffer.append(output)
            if console or manual:
                print(output, end="")


def main():
    with open("day25.txt", "r") as f:
        data = f.read().split(",")
    data = [int(x) for x in data]
    data = data + [0] * 10000
    print("\nPart 1: {}".format(run([], data)))


if __name__ == "__main__":
    main()
