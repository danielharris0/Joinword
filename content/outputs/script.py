import random
file = open('Processing/outputs/21_spelling.js','r')
lines = []
for line in file.readlines(): lines.append(line)
random.shuffle(lines)
file = open('Processing/outputs/21_spelling_random.js','w')
for line in lines: file.write(line)