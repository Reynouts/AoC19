# Advent of Code 2019
Solving puzzles of AoC19, probably all with Python.
In this readme, just some notes.

## Day 1
Easy puzzle today, took a couple of minutes to make it work
with a generator in a list comprehension. More straight-forward
solution would be a while loop and extra checks. Tried to make
it "pythonic". 

Notable part for this puzzle (is all the code for solving):
'''python
total = 0
while len(data) > 0:
   data = [i for i in (x // 3 - 2 for x in data) if i > 0]
   total += sum(data)
'''

## Day 2
Started with using a module to get my puzzle input automatically
without copy and pasting (just for fun, because I'm not waking 
up early enough for a leaderboard *attempt*). The module is 
called _advent-of-code-data_ (aocd). You can even make automatic
submissions, but I'm not touching that yet.

