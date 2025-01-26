import wn.morphy
import wordSplitter, wn, homophoneDict, copy, random, math

#TODO: A theory of valid non-chain topologies -- Consider chain ABCDE etc. We can add whatever links we like to B, since we know is predecessor 'A' is forced to connect.
#       In fact, (I think) for any LHS node in a chain, we can add arbitrary edges toward any RHS node 'below' it in the chain. Similarly for RHS nodes, we can add 'above'.

# In terms of actual construction though, if we are building the chain left -> right, then the fact of relevance is that LHS (odd) nodes can be connected to any previous RHS (even) node with impunity


SO_WHATS_GOING_ON = """"
    We add from top to bottom, left to right. So chain start is top left; chain end is bottom right.
    With this chain in mind, we can add any edges we like so long as we maintain the property that the 'chain' is the only valid solution. (Sort of inductive.)
    Therefore: consider the 'correct' link L <-> R in the chain... (This link is used in the solution)
        Above them we have L+ <-> R+
        And below we have L- <-> R-
        So the chain contains  ... L+ R+ L R L- R- ...



    When adding on the LEFT:
        The world is your oyster. Link with anything you like (anything above).

    When adding on the RIGHT:
        Add ZERO additional links (to anything above).


"""

def findSynonyms(word, excludedWords = set(), excludeSynsets = set()):
    synonyms = []
    for wnWord in wn.words(word):
        for synset in wnWord.synsets():
            if not synset in excludeSynsets:
                for lemma in synset.lemmas():
                    lemma = lemma.lower()
                    if not (lemma in synonyms) and not (lemma in excludedWords) and lemma!=word: synonyms.append(lemma)

                #'Related' words
                for relatedSynset in synset.get_related():
                    for lemma in relatedSynset.lemmas():
                        lemma = lemma.lower()
                        if not (lemma in synonyms) and not (lemma in excludedWords) and lemma!=word: synonyms.append(lemma)                       

    return synonyms

def findPossibleContinuations(word, excludedWords, excludeSynsets): #Only doing synonyms for now
    synonyms = findSynonyms(word, excludedWords, excludeSynsets)
    def countSynsets(x):
        n = 0
        for wnWord in wn.words(x): n+=len(wnWord.synsets())
        return n
    synonyms.sort(key = lambda x: - countSynsets(x))
    return synonyms

def homophones(word):
    if not word in homophoneDict.index: return set(word)
    else: return set(word).union(homophoneDict.index[word])

def printChain(chain, links):
    def listLinks(i):
        l = ''
        for j in range(len(links[i])):
            l += chain[links[i][j]]
            if j<len(links[i])-1: l+=', '
        l += ')'
        return l
    
    def node(i): return chain[i] + ' (' + listLinks(i)
    
    maxLength = 0
    for i in range(0,len(chain),2):
        maxLength = max(len(node(i)), maxLength)

    print('\n'*20 + '-'*maxLength*2)

    for i in range(math.ceil(len(chain)/2)):
        line = node(2*i)
        line += ' ' * (maxLength + 4 - len(line))
        if 2*i+1 < len(chain): line += node(2*i + 1)
        print(str(i+1) + ': ' + line)
    print('-'*maxLength*2)

def selectContinuation(chain, links, synonyms):
    charsPerLine = 150
    rowsPerPage = 10
    page = [[]]
    colWidths = []
    totalWidth = 0
    pageCutOff = False

    def calcLatestColWidth():
        nonlocal totalWidth
        longest = 0
        for l in page[-1]: longest = max(longest, len(l))
        colWidths.append(longest)
        totalWidth += longest

    def addItem(item):
        nonlocal totalWidth, pageCutOff

        if len(page[-1]) >= rowsPerPage:
            calcLatestColWidth()
            page.append([])

        if totalWidth + len(item) < charsPerLine: page[-1].append(item)
        else: pageCutOff = True

    n=0
    answer = ''

    while answer=='':
        page = [[]]
        colWidths = []
        totalWidth = 0
        pageCutOff = False

        if n >= len(synonyms): n=0

        while (n < len(synonyms) and not pageCutOff):
            addItem('[' + str(n+1) + '] ' + synonyms[n])
            n+=1

        calcLatestColWidth() #calc. width of last col
        if len(page[-1])==0: page.pop()


        print('\n'*20)
        printChain(chain, links)
        print('Options:' + (' (next page)' if pageCutOff else ''))
        for i in range(rowsPerPage):
            line = ''
            for j in range(len(page)):
                col = page[j]
                item = ''
                if i < len(col): item = col[i]
                line += item + (' ' * (colWidths[j] - len(item))) + '  |  '
            print(line)

        answer = input('[q:back  x:done  (-):custom] ')
    
    try:
        n = int(answer)
        return (True, synonyms[n-1])
    except:
        return (False, answer)

def generate(seedWord):
    
    def extend(chain, links, excludedR):
        #Determine the synset(s) used
        previousSynsets = set()
        if len(chain)>=2:
            wordA = chain[-2]
            wordB = chain[-1]
            for wnWord in wn.words(wordB):
                for synset in wnWord.synsets():
                    if wordA in synset.lemmas(): previousSynsets.add(synset)

        lastWord = chain[-1]
        allowRepeatedSynset = False

        while True:
            #re-find synonyms in case user changed search parameters
            synonyms = findPossibleContinuations(lastWord, set() if len(chain)%2==0 else excludedR, set() if allowRepeatedSynset else previousSynsets)

            (didPickAnOption, answer) = selectContinuation(chain, links, synonyms)

            if answer=='q': #back
                return None
            elif answer=='x' and len(chain)%2==0: #done
                return (chain, links)
            elif answer=='a':
                allowRepeatedSynset = not allowRepeatedSynset
            else:
                nextWord = answer

                extendedChain = chain + [nextWord]
                excludedRNew = copy.copy(excludedR)
                excludedRNew.add(nextWord) #That exact word is never used on either side again
                linksNew = copy.deepcopy(links) + [[len(chain)-1]]; linksNew[-2].append(len(chain))

                #Word chosen ... does it link to anything else??
                if not didPickAnOption and len(chain)%2==0 and len(chain)>2: #(If we're adding a LHS node)
                    printChain(chain, links)
                    answer = None
                    while answer!='':
                        answer = input('Does it link to anything else? ')
                        if answer!='':
                            try:
                                linksNew[-1].append((int(answer)*2)-1)
                                linksNew[(int(answer)*2)-1].append(len(linksNew)-1)
                                print('Okay.')
                            except:
                                pass

                if len(chain)%2==0:
                    excludedRNew = excludedRNew.union(set(findSynonyms(lastWord)))

                result = extend(extendedChain, linksNew, excludedRNew)
                if result != None: return result

    result = None
    while result==None: result = extend([seedWord], [[]], set([seedWord]))
    return result

def escapeQuotes(s):
    i=0
    while i<len(s):
        if s[i]=='\'' and (i==0 or s[i-1]!='\\'):
            s = s[:i] + '\\' + s[i:]
        i+=1
    return s

while True:
    seedWord = input('- ')
    (chain, links) = generate(seedWord)
    printChain(chain, links)

    left = []
    right = []
    answers = []
    for i in range(len(chain)):
        if i%2==0:
            left.append(escapeQuotes(chain[i]))
            answers.append([])
            for link in links[i]: answers[-1].append(int((link-1)/2))
        else: right.append(escapeQuotes(chain[i]))

    a = None; b = None
    while True:
        (s,a,b) = wordSplitter.applyPermutationToPuzzle(left, right, answers, a, b)
        print(s)
        print('Order:')
        for i in range(len(a)):
            l = left[a[i]]; r = right[b[i]]
            print(str(i) + ': ' + l + ' '*(30-len(l)) + r)

        response = input('To swap e.g. nodes 2 & 4 on the left, enter: L 2 4\n>')
        try:
            response = response.lower().split(' ')
            assert(len(response)==3)
            assert(response[0] in ['l','r'])
            n1 = int(response[1]); n2 = int(response[2])
            assert(n1 in range(0,len(a))); assert(n2 in range(0, len(b)))
            if response[0]=='l':
                temp = a[n1]
                a[n1] = a[n2]
                a[n2] = temp
            else:
                temp = b[n1]
                b[n1] = b[n2]
                b[n2] = temp
        except:
            pass