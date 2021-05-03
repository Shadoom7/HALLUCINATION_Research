import os
import sys

count = 0
file = open('corpus.val.zh', 'r')
target = open('corpus.val.char.zh', 'w')
for line in file:
    for char in line:
        if char == '\n':
            target.write(char)
        elif char != ' ':
            target.write(char+' ')
        else:
            target.write('@@ ')

