import copy, random, nltk, wordlist

(words, allWords) = wordlist.get(1,12)
MIN_FREQ = 2 #min frequency of a prefix/suffix to be recorded
puzzleSize = 11

prefixes = {} #dictionary of sets
suffixes = {} #dictionary of sets

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

print("Split words")

def growChain(inputChain, limit = 10):
    if (len(inputChain)==0):
        while True:
            prefix = random.choice(list(prefixes))
            if prefixes[prefix]!=None:
                success, newChain = growChain([prefix], limit)
                if success: return (True, newChain)

    if (len(inputChain)>=limit):
        return (True, inputChain)
    
    chain = copy.copy(inputChain)

    if len(chain)%2==0:
        #Find a prefix that links to the previous suffix and not to any others
        l = list(suffixes[chain[-1]])
        random.shuffle(l)
        for prefix in l:
            if prefixes[prefix]!=None and not (prefix in chain):
                valid = True
                for i in range(1, len(chain)-2, 2):
                    if prefix+chain[i] in allWords:
                        valid = False
                        break
                if valid:
                    success, newChain = growChain(chain + [prefix], limit)
                    if success: return (True, newChain + [prefix])
        return (False, None)

    else:
        #Find a suffix that links to the previuous prefix and not to any others
        l = list(prefixes[chain[-1]])
        random.shuffle(l)
        for suffix in l:
            if suffixes[suffix]!=None and not (suffix in chain):
                valid = True
                for i in range(0, len(chain)-2, 2):
                    if chain[i]+suffix in allWords:
                        valid = False
                        break
                if valid:
                    success, newChain = growChain(chain + [suffix], limit)
                    if success: return (True, newChain + [suffix])
        return (False, None)
    
def generatePuzzleListingFromChain(chain, a=None, b=None):
    print('\n')
    print(chain)

    print()
    for i in range(0,len(chain),2):
        if i>0: print(chain[i] + chain[i-1], end="  ")
        print(chain[i] + chain[i+1], end="  ")
    print()

    l = int(len(chain)/2)

    if a==None:
        a = list(range(l))
        random.shuffle(a)

    if b==None:
        b = list(range(l))
        random.shuffle(b)

    permutation = [None]*len(chain) #Converts 'chain index' to 'puzzle index' 

    for i in range(len(chain)):
        if i%2==0: #prefix
            permutation[i] = a[int(i/2)]
        else:
            permutation[i] = b[int((i-1)/2)]

    reversePermutation_Prefix = [None]*l #Converts 'puzzle index' of a prefix back to its 'chain index'
    for i in range(l):
        for j in range(len(chain)):
            if j%2==0 and permutation[j]==i: reversePermutation_Prefix[i] = j 

    reversePermutation_Suffix = [None]*l #Converts 'puzzle index' of a suffix back to its 'chain index'
    for i in range(l):
        for j in range(len(chain)):
            if j%2==1 and permutation[j]==i: reversePermutation_Suffix[i] = j 

    s = "new Puzzle(["
    for i in range(l): s+='\''+chain[reversePermutation_Prefix[i]]+'\''+','
    s=s[:-1]+'],['
    for i in range(l): s+='\''+chain[reversePermutation_Suffix[i]]+'\''+','
    s=s[:-1]+'],['
    for i in range(l):
        chainIndex = reversePermutation_Prefix[i]
        if chainIndex==0: s += '[' + str(permutation[1]+1) + '],'
        else: s += '[' + str(permutation[chainIndex-1]+1) + ',' + str(permutation[chainIndex+1]+1) + '],'
    s=s[:-1]+']),'

    print()
    input(s)

#generatePuzzleListingFromChain([])

chainLength = puzzleSize * 2
while True:
    (result, c) = growChain([],chainLength)
    generatePuzzleListingFromChain(c[:chainLength])