words = {}

with open('freq.dat','r') as file:
    for line in file.readlines():
        try:
            [word, freq, cd] = line.split('	')
            word = word.lower().strip('-')
            if not word in words: words[word] = 0
            words[word] += int(freq)
        except:
            pass


with open('frequentNouns.csv','w') as file:
    for word in words:
        if words[word]>500:
            file.write(word+'\n')