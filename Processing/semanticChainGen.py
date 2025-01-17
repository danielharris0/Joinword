import wn.morphy
import wordSplitter, wn, homophoneDict, copy, random, math

#TODO: A theory of valid non-chain topologies -- Consider chain ABCDE etc. We can add whatever links we like to B, since we know is predecessor 'A' is forced to connect.
#       In fact, (I think) for any LHS node in a chain, we can add arbitrary edges toward any RHS node 'below' it in the chain. Similarly for RHS nodes, we can add 'above'.

# In terms of actual construction though, if we are building the chain left -> right, then the fact of relevance is that LHS (odd) nodes can be connected to any previous RHS (even) node with impunity

#wn.download('ewn:2020')
#wordnet = wn.Wordnet('ewn:2020')
#extendedWordnet = wn.Wordnet('ewn:2020', lemmatizer=wn.morphy.Morphy()) #ewn:2020 extended with a lemmatizer s.t. e.g. 'jumped' can be recognised as 'jump'

def findSynonyms(word, excludedWords = set(), excludeSynsets = set()):
    synonyms = []
    for wnWord in wn.words(word):
        for synset in wnWord.synsets():
            if not synset in excludeSynsets:
                for lemma in synset.lemmas():
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

while True:
    seedWord = input('- ')
    (chain, links) = generate(seedWord)
    printChain(chain, links)

    left = []
    right = []
    answers = []
    for i in range(len(chain)):
        if i%2==0:
            left.append(chain[i])
            answers.append([])
            for link in links[i]: answers[-1].append(int((link-1)/2))
        else: right.append(chain[i])

    if input('Specify order? ')=='y':
        while True:
            printChain(chain, links)
            a = []
            for i in range(len(left)): a.append(int(input('LEFT: What should go in position ' + str(i+1) + '? ')) - 1)

            printChain(chain, links)
            b = []
            for i in range(len(left)): b.append(int(input('RIGHT: What should go in position ' + str(i+1) + '? ')) - 1)

            try:
                wordSplitter.applyPermutationToPuzzle(left, right, answers, a, b)
            except:
                print('Bad format')
                pass
    else:
        while True:
            wordSplitter.applyPermutationToPuzzle(left, right, answers)


    plan = """"



    """