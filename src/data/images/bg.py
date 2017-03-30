import os
import sys

for img in os.listdir('negatives'):
    line = 'negatives/' + img + '\n'
    with open('bg.txt', 'a') as f:
        f.write(line)
