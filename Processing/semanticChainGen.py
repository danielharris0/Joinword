import wn.morphy
import wordSplitter, wn, homophoneDict, copy, random

#TODO: A theory of valid non-chain topologies -- Consider chain ABCDE etc. We can add whatever links we like to B, since we know is predecessor 'A' is forced to connect.
#       In fact, (I think) for any LHS node in a chain, we can add arbitrary edges toward any RHS node 'below' it in the chain. Similarly for RHS nodes, we can add 'above'.

wn.download('ewn:2020')
wordnet = wn.Wordnet('ewn:2020')
#extendedWordnet = wn.Wordnet('ewn:2020', lemmatizer=wn.morphy.Morphy()) #ewn:2020 extended with a lemmatizer s.t. e.g. 'jumped' can be recognised as 'jump'

def findPossibleLinks(word, excludeSynsets = set()):
    links = []

    #Homophones
    if word in homophoneDict.index: links += homophoneDict.index[word]

    #Synonyms
    for wnWord in wn.words(word):
        for synset in wnWord.synsets():
            if not synset in excludeSynsets:
                for lemma in synset.lemmas():
                    if not (lemma in links): links.append(lemma)

    #Category relations
    #for wnWord in wn.words(word):
    #    for synset in wnWord.synsets():            
    #        for hypernym in synset.hypernyms(): links += hypernym.lemmas()
    #        for hyponym in synset.hyponyms(): links += hyponym.lemmas()
    
    return links


def findPossibleContinuations(word, excludedWords, excludeSynsets):
    links = []
    for link in findPossibleLinks(word, excludeSynsets):
        if (not (link in excludedWords)): links.append(link)
    return links

def generate(seedWord):
    
    def extend(chain, excludedL, excludedR):
        #Determine the synset(s) used (if it was a synonym-type link)
        previousSynsets = set()
        if len(chain)>=2:
            wordA = chain[-2]
            wordB = chain[-1]
            for wnWord in wn.words(wordA):
                for synset in wnWord.synsets():
                    if wordB in synset.lemmas(): previousSynsets.add(synset)

        lastWord = chain[-1]
        options = findPossibleContinuations(lastWord, excludedL if len(chain)%2==0 else excludedR, previousSynsets)

        while True:

            print('Length: ' + str(len(chain)/2))
            print(chain)
            print('Options:')
            
            page = 0
            chosenOption = None 
            while (chosenOption == None):
                print(str((page*9)+1) + ' of ' + str(len(options)) + ':')
                for i in range(0,9):
                    index = page*9 + i
                    if index < len(options):
                        print('['+str(i+1)+'] ' + options[index])
                answer = input('- ')
                if answer.isdigit() and int(answer)>=1 and int(answer)<=9:
                    chosenOption = options[page*9 + int(answer) - 1] 
                elif answer=='q':
                    return None
                elif answer=='x' and len(chain)%2==0:
                    return chain
                elif answer=='':
                    page+=1
                    if page*9 + 1 >= len(options): page = 0
                    print(chain)
                else:
                    chosenOption = answer

            extendedChain = chain + [chosenOption]
            excludedLNew = copy.copy(excludedL); excludedRNew = copy.copy(excludedR)
            excludedLNew.add(chosenOption); excludedRNew.add(chosenOption) #That exact word is never used on either side again
            if len(chain)%2==0: excludedRNew = excludedRNew.union(set(findPossibleLinks(lastWord)))
            else: excludedLNew = excludedLNew.union(set(findPossibleLinks(lastWord)))

            completedChain = extend(extendedChain, excludedLNew, excludedRNew)
            if completedChain != None: return completedChain

    return extend([seedWord], set([seedWord]), set([seedWord]))

while True:
    seedWord = input('- ')
    chain = generate(seedWord)
    print(chain)
    wordSplitter.generatePuzzleListingFromChain(chain)