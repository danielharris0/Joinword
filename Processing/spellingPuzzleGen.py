#todo: fix dictionary issue e.g. no 'paw', 'sting', or 'hive'

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
#PRECOMPUTE ALL PREFIXES and SUFFIXES of the complete wordlist
allPrefixes = {} #dictionary of sets
allSuffixes = {} #dictionary of sets

def precompute():
    global prefixes, suffixes, allPrefixes, allSuffixes

    for word in allWords:
        for i in range(0,len(word)+1):
            prefix = word[:i]
            suffix = word[i:]

            if not (prefix in allPrefixes): allPrefixes[prefix] = set()
            if not (suffix in allSuffixes): allSuffixes[suffix] = set()

            allPrefixes[prefix].add(suffix)
            allSuffixes[suffix].add(prefix)

    for prefix in allPrefixes: prefixes[prefix] = set()
    for suffix in allSuffixes: suffixes[suffix] = set()

    for word in words:
        for i in range(0,len(word)+1):
            prefix = word[:i]
            suffix = word[i:]

            prefixes[prefix].add(suffix)
            suffixes[suffix].add(prefix)

    # Remove uncommon prefixes / suffixes from the positive case
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

def generateAnswers(L,R):
    answers = []
    for l in L:
        links = []
        for i in range(len(R)):
            if R[i] in allPrefixes[l]:
                links.append(i)
        answers.append(links)
    return answers

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
                    if prefix!=prevPrefix and prefix in allSuffixes[suffix]:
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
            if success:
                return (L, R)

def logPuzzle(L,R,answers):
   # print('Left:',L)
   # print('Right:',R)
    validWords = []
    for l in range(len(L)):
        for r in answers[l]:
            validWords.append(L[l]+R[r])
    
    invalidWords = []
    for l in range(len(L)):
        for r in set(range(len(R))).difference(set(answers[l])):
            invalidWords.append(L[l]+R[r])


    print('Valid:', validWords)
    print('Invalid:', invalidWords)


file = open('Processing/output','w')

i = 0
while i<1000:
    n = random.randint(1,6)
    if random.randint(0,1)==0:
        prefixLengthRange = rangeInc(n,n)
        suffixLengthRange = rangeInc(1,12)
    else:
        prefixLengthRange = rangeInc(1,12)
        suffixLengthRange = rangeInc(n,n)

    (L, R) = generatePuzzle()
    if calcNumBacklinks(L,R)>=4:
        answers = generateAnswers(L,R)
        #logPuzzle(L,R,answers); input()
        file.write(wordSplitter.applyPermutationToPuzzle(L, R, answers)[0] + '\n')
        i+=1
        print(i)