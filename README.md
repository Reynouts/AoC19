# Advent of Code 2019
Solving puzzles of AoC19, probably all with Python.
In this readme, just some notes. 

## Day 1
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

## Day 2
Started with using a module to get my puzzle input automatically
without copy and pasting (just for fun, because I'm not waking 
up early enough for a leaderboard *attempt*). The module is 
called [advent-of-code-data (aocd)](https://github.com/wimglenn/advent-of-code-data). 
You can even make automatic submissions, but I'm not touching that yet.

Today's puzzle was a bit harder to read, but the solution was
straight forward. Bruteforce worked in Python to find the two
paramters. It would be fun to fit the parameters smarter with
some kind of binary search algorithm, but I didn't wrap my head
around that and probably it wouldn't even work.

Got some errors to start with, because I was manipulating the
list and in the next iteration, starting with the manipulated array.
To fix that, I had to initialize the list every iteration of course.
Did that with a deepcopy of the initial list.

## Day 3
This puzzle reminded me of the "Minecart Madness" puzzle of last year,
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