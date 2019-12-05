# Advent of Code 2019
Solving puzzles of AoC19, probably all with Python.
In this readme, just some notes. 

## [--- Day 1: The Tyranny of the Rocket Equation ---](https://adventofcode.com/2019/day/1)
Easy puzzle today, took a couple of minutes to make it work
with a generator in a list comprehension. More straight-forward
solution would be a while loop and extra checks. Tried to make
it "pythonic" and short.

Notable part for this puzzle (is all the code for solving):
``` python
total = 0
while len(data) > 0:
   data = [i for i in (x // 3 - 2 for x in data) if i > 0]
   total += sum(data)
```

## [--- Day 2: 1202 Program Alarm ---](https://adventofcode.com/2019/day/2)

Started with using a module to get my puzzle input automatically
without copy and pasting (just for fun, because I'm not waking 
up early enough for a leaderboard *attempt*). The module is 
called [advent-of-code-data (aocd)](https://github.com/wimglenn/advent-of-code-data). 
You can even make automatic submissions, but I'm not touching that yet.

This puzzle was insipred by the Apollo Guidance Computer, which
used two parameters to activate a command, consisting of a mapping
between a number and a verb and a number and a noun.

Today's puzzle was a bit harder to read, but the solution was
straight forward. Bruteforce worked in Python to find the two
paramters. It would be fun to fit the parameters smarter with
some kind of binary search algorithm, but I didn't wrap my head
around that and probably it wouldn't even work.

Got some errors to start with, because I was manipulating the
list and in the next iteration, starting with the manipulated array.
To fix that, I had to initialize the list every iteration of course.
Did that with a deepcopy of the initial list.

## [--- Day 3: Crossed Wires ---](https://adventofcode.com/2019/day/3)
This puzzle reminded me of the "[Mine cart madness](https://adventofcode.com/2018/day/13)" puzzle of last year,
running a cart through a grid and calculating where carts would crash
with each other.

This time it are no carts, but wires that could be intersected. Part 1
was searching for the closest intersection with the manhattan distance.
Second part you should account for the total number of steps covered by
the wires. From part 1 to part 2, it was a change from a list to a dict.

Still no fancy solutions, straight forward did the job just fine. Some
smart trick that I saw from a fellow-AOCer was using a dictionary to
change directions instead of a ugly `if/elif` construction.

``` python
if heading == "R":
    dxy = (1,0)
elif heading == "L":
    dxy = (-1,0)
=elif heading == "U":
    dxy = (0,-1)
elif heading == "D":
    dxy = (0,1)
```

Could be:

``` python
deltas = {'R': (1, 0), 'L': (-1, 0), 'U': (0, 1), 'D': (0, -1)}
# ...
dxy = deltas[heading]
```

Which is a lot nicer and easier to expand.

## [--- Day 4: Secure Container ---](https://adventofcode.com/2019/day/4)
So today the puzzle was to generate 6-digit-numbers between two
given input numbers and decide if this number was a valid password.
Valid means:

- All digits must be ascending or equal to the previous digit
- There must be a group of two of the same digits in the number
- For part 2: a group of three or more of the same digits does not count, so it needs to be a group of exactly two of the same digits

Not too hard day either, but needed some juggling with booleans and
if/elis constructions after it worked. After my train ride to work
I figured out the problem was more restricted than I tought and I
came up with a easier solution:

``` python
# After understanding the requirements better, this does a nicer job solving it.
# Sorting the array and checking if is equal, means it is increasing in number
# After that it is possible to do counts for the number, because it is sorted it
# is not possible to get something like 223324 in the input (which would work with
# my original solution, but was not the question). That's why a simple count works.
def solve(data):
    candidates = []
    for x in range(data[0], data[1]):
        rep = str(x)
        if "".join(sorted(rep)) == rep:
            for i in set(rep):
                if rep.count(i) == 2:
                    candidates.append(x)
                    break
    print ("Part 2: {}".format(len(candidates)))
```

Even a more pythonic solution from a fellow AoCer to check if a password is a candidate for part 1:

``` python
def is_password(num):
    s = str(num)
    adjacent = any(a == b for a, b in zip(s, s[1:]))
    monotonic = all(a <= b for a, b in zip(s, s[1:]))
    return adjacent and monotonic
```

I wouldn't come up with that solution, very nice and short.


But the most funny thing today was Roland's bad ass solution:

``` python
passwords = list()
for i in range(1, 7):
    for j in range(i, 10):
        for k in range(j, 10):
            for l in range(k, 10):
                for m in range(l, 10):
                    for n in range(m, 10):
                        number = int(''.join([str(i),str(j),str(k),str(l),str(m),str(n)]))
                        if number >= 138241 and number <= 674034 and (i==j or j==k or k==l or l==m or m==n):
                            passwords.append(number)
print(len(passwords))
```

Pythonic, eh? :')

## [--- Day 5: Sunny with a Chance of Asteroids ---](https://adventofcode.com/2019/day/5)

Today we continued where we left of in day 2. The task was to expand the 
Intcode computer with a diagnostics program. This involved some thorough
reading, adding some functions corresponding to *opcodes* and figuring 
out which number needs to be submitted after the program terminates.

This kind of assembly-like puzzles were also present last year, and 
these aren't my favorites, because if you have read and undestood the 
assignment, the implementation is quite straight-forward. There are no
algorithmic challenges involved, just "more of the same".

One thing I learned today from was formatting a integer, so it got 
leading zero's. This is easily done with f-strings:

``` python
>>> f"{1:04}
'0001'
>>> f"{103:04}
'0103'
>>> f"{1101:04}
'1101'
```

This way you convert it to a string with the "width" you need.

Next!
