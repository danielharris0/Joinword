import nltk

def loadWordList(filename, minLength, maxLength):#
    file = open(filename,'r')
    words = set()
    for line in file.readlines():
        word = line.split('\n')[0].split('	')[0].lower()
        if len(word)>=minLength and len(word)<=maxLength:
            words.add(word)
    return words

def get(minLength,maxLength):
    a = loadWordList('Processing/words.txt', minLength, maxLength)
    b = loadWordList('Processing/google10k.txt', minLength, maxLength)
    c = loadWordList('Processing/michigan_words.txt', minLength, maxLength)
    d = set(nltk.corpus.words.words())
    e = loadWordList('Processing/collins_scrabble_2019.txt', minLength, maxLength)
    f = loadWordList('Processing/20k.txt', minLength, maxLength)

    safeWords = f.intersection(e.intersection(a.intersection(c).union(a.intersection(d)))) #Definitely known by the solver


    allWords = a.union(b).union(c).union(d) #Might be known by the solver

    print('Loaded Words')
    return (safeWords, allWords)

