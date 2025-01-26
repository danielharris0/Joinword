import copy, random, wordlist, wordSplitter

#SETTINGS:
MIN_FREQ = 2 #min frequency of a prefix/suffix to be recorded
puzzleSize = 6 #number of nodes on each side of the puzzle
(words, allWords) = wordlist.get(1,12)

def rangeInc(start, stop): return range(start, stop+1)
prefixLengthRange = rangeInc(4,4)
suffixLengthRange = rangeInc(0,12)

def prefixGood(word): return len(word) in prefixLengthRange
def suffixGood(word): return len(word) in suffixLengthRange

#PRECOMPUTE ALL PREFIXES and SUFFIXES of the common wordlist
prefixes = {} #dictionary of sets
suffixes = {} #dictionary of sets


def precompute():
    global prefixes, suffixes
    for word in words:
        for i in range(0,len(word)+1):
            prefix = word[:i]
            suffix = word[i:]

            if not (prefix in prefixes): prefixes[prefix] = set()
            if not (suffix in suffixes): suffixes[suffix] = set()

            prefixes[prefix].add(suffix)
            suffixes[suffix].add(prefix)

    # Remove uncommon prefixes / suffixes
    prefixes = {k: v for k, v in prefixes.items() if len(v)>=MIN_FREQ}        
    suffixes = {k: v for k, v in suffixes.items() if len(v)>=MIN_FREQ}
    for prefix in prefixes: prefixes[prefix] = {suffix for suffix in prefixes[prefix] if suffix in suffixes}
    for suffix in suffixes: suffixes[suffix] = {prefix for prefix in suffixes[suffix] if prefix in prefixes}
precompute()

print("Precomputed")

#Grow a puzzle using the 'chain method':
#1. Find a prefix linking to the last suffix (and possibly to *ANY* PREVIOUS suffix)
#2. Find a suffix linking to the last prefix (and to *NO* PREVIOUS prefixes)
# repeat...
# The only valid solution will be to link the nth prefix with the nth suffix.

def calcNumBacklinks(L, R):
    numBacklinks = 0
    for i in range(len(L)):
        prefix = L[i]
        n = 0
        for j in range(i-1):
            suffix = R[j]
            if suffix in prefixes[prefix]: n+=1
        numBacklinks += n
    return numBacklinks

def generatePuzzle():
    def extendPuzzle(L, R): #recursively tries to extend the puzzle; returns (success, L', R') with the success flag and the expanded lists
        L = copy.copy(L)
        R = copy.copy(R)

        if (len(L)==puzzleSize and len(R)==puzzleSize):
            return (True, L, R)

        if len(L) == len(R): #add a prefix
            prevSuffix = R[-1]

            #Find the option that links with the most previous suffixes
            options = []
            for prefix in suffixes[prevSuffix]:
                if not prefix in L and prefixGood(prefix): options.append({'word': prefix, 'numLinks': 0})

            #Calculate numlinks for each
            for option in options:
                n = 0
                for suffix in R:
                    if suffix in prefixes[prefix]: n+=1
                option['numLinks'] = n

            random.shuffle(options) #remove bias 
            options.sort(key = lambda option: option['numLinks'])

            for option in options:
                (success, Lnew, Rnew) = extendPuzzle(L + [option['word']], R)
                if success: return (success, Lnew, Rnew)

        elif len(L) > len(R): #add a suffix
            prevPrefix = L[-1]
            options = list(prefixes[prevPrefix])
            options = [option for option in options if not option in R and suffixGood(option)]

            #Remove all options with links to previous prefixes
            for i in range(len(options)-1, -1, -1):
                suffix = options[i]
                for prefix in L:
                    if prefix!=prevPrefix and prefix in suffixes[suffix]:
                        del options[i]
                        break

            random.shuffle(options) #remove bias 

            for option in options:
                (success, Lnew, Rnew) = extendPuzzle(L, R + [option])
                if success: return (success, Lnew, Rnew)

        else:
            assert(False)

        return (False, L, R)
    while True:
        start = random.choice(list(prefixes))
        if prefixGood(start):
            (success, L, R) = extendPuzzle([start], [])
            if success: return (L, R)

maxReuseSeen = 0 


lenL = 4; lenR = 1
prefixLengthRange = rangeInc(lenL,lenL)
suffixLengthRange = rangeInc(0,12)

file = open('Processing/outputs/240_spelling_puzzles','a')

for lenL in rangeInc(3,3):
    allL = set()
    allR = set()
    prefixLengthRange = rangeInc(lenL,lenL)
    numPuzzles = 0
    while numPuzzles < 2:
        (L, R) = generatePuzzle()
        if calcNumBacklinks(L,R)>=6:
            reuse = (len(allL.intersection(set(L))) + len(allR.intersection(set(R)))) / (puzzleSize*2)
            reuseDelta = abs(maxReuseSeen - reuse)

            if reuse < 0.5 and reuseDelta < 0.1: #it would be inefficient to increase reuse too quickly

                answers = []
                for l in L:
                    links = []
                    for i in range(len(R)):
                        if R[i] in prefixes[l]:
                            links.append(i)
                    answers.append(links)
                
                wordsUsed = []
                for i in range(len(L)): wordsUsed.append(L[i] + R[i])

                print((reuse, calcNumBacklinks(L,R), numPuzzles, L, R))
                file.write(wordSplitter.applyPermutationToPuzzle(L, R, answers) + '\n')
                allL = allL.union(set(L))
                allR = allR.union(set(R))
                maxReuseSeen = max(maxReuseSeen, reuse)
                numPuzzles+=1


