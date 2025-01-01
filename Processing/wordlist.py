import nltk

def loadWordList(filename):#
    file = open(filename,'r')
    words = set()
    for line in file.readlines():
        word = line.split('\n')[0]
        if (len(word)>=4):
            words.add(word)
    return words

def get():
    a = loadWordList('Processing/words.txt')
    b = loadWordList('Processing/google10k.txt')
    c = loadWordList('Processing/michigan_words.txt')
    d = set(nltk.corpus.words.words())

    safeWords = a.intersection(b).intersection(c).intersection(d) #Definitely known by the solver
    allWords = a.union(b).union(c).union(d) #Might be known by the solver

    print('Loaded Words')
    return (safeWords, allWords)

