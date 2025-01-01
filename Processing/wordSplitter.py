import copy, random, nltk, wordlist

M = 2 #a suffix must appear at least M times to be counted

(words, allWords) = wordlist.get()

file = open('Processing/prefixes.csv','r')
prefixes = {}
for line in file.readlines():
    prefix = line.split('\"')[1]
    prefixes[prefix] = set()
#prefixes[''] = set()
print('Loaded Prefixes')

suffixes = {}
for word in words:
    for i in range(len(word)+1):
        prefix = word[:i]
        if prefix in prefixes:
            suffix = word[i:]
            if suffix in suffixes: suffixes[suffix]+=1
            else: suffixes[suffix] = 1
print('Found suffixes')

for word in words:
    for i in range(len(word)+1):
        prefix = word[:i]
        if prefix in prefixes:
            suffix = word[i:]
            if suffixes[suffix]>=M:
                prefixes[prefix].add(suffix)

print('Found true suffixes')

suffixes = {}
for prefix in prefixes:
    for suffix in prefixes[prefix]:
        if not(suffix in suffixes): suffixes[suffix] = set()
        suffixes[suffix].add(prefix)
print('Indexed suffixes')

#Remove under a certain length
minLength = 3
for prefix in prefixes: 
    if len(prefix)<minLength: prefixes[prefix] = None
for suffix in suffixes: 
    if len(suffix)<minLength: suffixes[suffix] = None

for i in range(10):

    for prefix in prefixes:
        if prefixes[prefix]!=None and len(prefixes[prefix])<M:
            prefixes[prefix] = None
            for suffix in suffixes:
                if suffixes[suffix]!=None and prefix in suffixes[suffix]: suffixes[suffix].remove(prefix)

    for suffix in suffixes:
        if suffixes[suffix]!=None and len(suffixes[suffix])<M:
            suffixes[suffix] = None
            for prefix in prefixes:
                if prefixes[prefix]!=None and suffix in prefixes[prefix]:
                    prefixes[prefix].remove(suffix)


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
    
def generatePuzzleListingFromChain(chain):
    print(chain)

    l = int(len(chain)/2)
    a = list(range(l))
    b = list(range(l))

    random.shuffle(a)
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

puzzleSize = 6
chainLength = puzzleSize * 2
while True:
    (result, c) = growChain([],chainLength)
    generatePuzzleListingFromChain(c[:chainLength])