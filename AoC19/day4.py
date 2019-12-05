def check(number):
    rep = str(number)
    last = "0"
    match, twice, found = False, False, False
    for i in rep:
        if int(i) < int(last):
            return False
        if i == last:
            if match:
                twice = False
            else:
                match, twice = True, True
        else:
            if twice and match:
                found = True
            match, twice = False, False
        last = i
    return found or (twice and match)


def solve(data):
    candidates = []
    for number in range(data[0], data[1]):
        if check(number):
            candidates.append(number)
    print ("Part 2: {}".format(len(candidates)))


'''
# After understanding the requirements better, this does a nicer job solving it.
# Sorting the array and checking if is equal, means it is increasing in number
# After that it is possible to do counts for the number, because it is sorted it
# is not possible to get something like 223324 in the input (which would work with
# my original solution, but was not the question). That's why a simple count works.
def solve(data):
    candidates = []
    for x in range(data[0], data[1]):
        rep = str(x)
        if rep == "".join(sorted(rep)):
            for i in set(rep):
                if rep.count(i) == 2:
                    candidates.append(x)
                    break
    print ("Part 2: {}".format(len(candidates)))
'''


def main():
    data = (235741, 706948)
    solve(data)


if __name__ == "__main__":
    main()