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
   # michigan = loadWordList('Processing/michigan_words.txt', minLength, maxLength)
    scrabble = loadWordList('Processing/collins_scrabble_2019.txt', minLength, maxLength)
    nltkWords = set(nltk.corpus.words.words())
    michigan_wordsWithVariants = set(loadWordList('Processing/OED_Processor/michigan_words_Out.txt', minLength, maxLength))
    iweb_60000 = set(loadWordList('Processing/OED_Processor/iweb_60000_Out.txt', minLength, maxLength))

    rudeWords = set(loadWordList('Processing/badWords.txt', 0, 50))

    game = set(loadWordList('Processing/12dicts-6.0.2/International/3of6game.txt', 0, 50))

    safeWords = michigan_wordsWithVariants.intersection(iweb_60000).intersection(game).difference(rudeWords) #michigan.intersection(scrabble.intersection(common.intersection(nltkWords))) #Definitely known by the solver
    allWords = safeWords.union(scrabble) #Might be known by the solver

    assert('hive' in allWords)

    assert('bled' in safeWords)
    assert('paw' in safeWords)
    assert('sting' in safeWords)
    assert('wove' in safeWords)
    assert('hive' in safeWords)
    
    assert(not 'jupe' in safeWords)
    assert(not 'carl' in safeWords)
    assert(not 'erg' in safeWords)
    assert(not 'guar' in safeWords)
    assert(not 'fuck' in safeWords)
    assert(not 'ling' in safeWords)
   # assert(not 'pix' in safeWords)
    assert(not 'nee' in safeWords)

    assert('pec' in allWords)


    print('Loaded Words')
    return (safeWords, allWords)
