import wn, random, homophoneDict, wn.similarity

#Docs: https://wn.readthedocs.io/en/latest/api/wn.htm


wn.download('oewn:2024') #(Open English Wordnet)

def findWord(shouldLink, shouldNotLink, avoidSpellings):
    def test(label):
        #Not exact spelling
        for otherLabel in avoidSpellings:
            if label.sameSpelling(otherLabel): return None

        #Must link
        for i in range(1, len(shouldLink)):
            linkLabel = shouldLink[i]
            if not label.links(linkLabel): return None

        #Must not link
        for i in range(0, len(shouldNotLink)):
            antiLinkLabel = shouldNotLink[i]
            if label.links(antiLinkLabel): return None

        return label


    for label in enumerateLinks(shouldLink[0]):
        result = test(label)
        if result!=None:
            return result
    



#With link A-B-C link A-B needs to explicitly use a DIFFERENT SENSE to link B-C.
#Clues might also be clearer if they specify the nature of the relationship?    
# 
# 
# BUG:     ['rhabdomancer', 'dowser', 'divining rod', 'dowsing rod'] ::          findWord(['divining rod'],['dowser'],[]) should not yeild 'downsing rod', as this is synonymous to 'dowser'

def printChain(chain):
    s = "["
    for i in range(len(chain)):
        s += chain[i].spelling
        if i<len(chain)-1: s+=", "
    s += "]"
    print(s)

def enumerateLinks(label):
    links = []


    for homophoneSpelling in label.homophoneSpellings: links.append(Label(homophoneSpelling))

    for synset in label.synsets:
        for word in synset.words():
            links.append(Label(word.lemma()))

        for hypernym in synset.hypernyms():
            for word in hypernym.words():
                links.append(Label(word.lemma()))

        for hyponym in synset.hyponyms():
            for word in hyponym.words():
                links.append(Label(word.lemma()))

    random.shuffle(links)
    while (len(links)>0): yield links.pop()

class Label:
    def __init__(self,spelling):
        self.spelling = spelling
        self.synsets = set()
        self.forms = set()
        self.homophoneSpellings = []
        if spelling in homophoneDict.index: self.homophoneSpellings = homophoneDict.index[spelling]
        for word in wn.words(spelling):
            #Only include synsets for words of which 'spelling' is the canonical form (otherwise Label('caught') will include the synsets for 'catch', including synonyms like 'hitch', 'exception' etc.)
            if spelling == word.lemma():
                for synset in word.synsets():
                    self.synsets.add(synset)

            for form in word.forms(): self.forms.add(form)


    def __str__(self): return self.spelling

    def links(self, that):   
        #Test if A is a kth hypernym of B or vise-versa
        for synsetA in self.synsets:
            for synsetB in that.synsets:
                lchns = wn.taxonomy.lowest_common_hypernyms(synsetA, synsetB)
                if synsetA in lchns or synsetB in lchns:
                    return True
                
        return len(self.synsets.intersection(that.synsets))>0 or (self.spelling in that.homophoneSpellings) #TODO: faster
    
    def sameSpelling(self, that):
        return len(self.forms.intersection(that.forms))>0 #TODO: faster


def buildChain(chain):
    if len(chain)>=100: return chain

    notRelatedTo = []
    for i in range(0,len(chain)-1):
        if i%2==len(chain)%2-1:
            notRelatedTo.append(chain[i])

    word = findWord([chain[-1]], notRelatedTo, chain)
    if word!=None:
        chain.append(word)
        return buildChain(chain)
    else:
        return chain
    
def printSynonyms(form):
    synonyms = set()
    for word in wn.words(form):
        for synset in word.synsets():
            for synonym in synset.words(): synonyms.add(synonym.lemma())
    print(synonyms)


frequentNouns = []
with open('frequentNouns.csv','r') as file:
    for line in file.readlines():
        frequentNouns.append(line.strip('\n'))
    
def similarity(a,b):
    total = 0
    for synsetA in a.synsets:
        for synsetB in b.synsets:
            if synsetA.pos == synsetB.pos:
                total += wn.similarity.path(synsetA, synsetB)
    return total

#print(similarity(Label('caught'), Label('hitch')))
#print(similarity(Label('hang-up'), Label('hitch')))

#for i in range(10000):
#    word = random.choice(frequentNouns)
#    chain = buildChain([Label(word)])
#    if (len(chain)>=12): printChain(chain)

def startChainFromWordList(words):
    words = words.split(', ')
    chain = []
    for word in words: chain.append(Label(word))
    return chain

for word in enumerateLinks(Label('recite')): print(word.spelling)

word = random.choice(frequentNouns)
while True:
    chain = buildChain(startChainFromWordList('slight, thin, lean, list, itemise, recite'))
    printChain(chain)
    input('')


#ISSUES:
#1. Tenuous links (is there a way to check sense frequency?)
#2. synonym-type links that sound too much like the original are not interesting (e.g. fantasy-fancy; or "take to"-take)

#TODO: Use hypernym_paths to aknowledge thta e.g. 'piano' links with 'instrument' even though it is more than one hypernym-level deep

#TRY just manually calling makeChain([...]) with a half-completed chain whenever it gets stuck (simulated backtracking)