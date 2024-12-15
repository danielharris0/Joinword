import wn, random

#Docs: https://wn.readthedocs.io/en/latest/api/wn.htm


wn.download('oewn:2024') #(Open English Wordnet)

def findWord(shouldLink, shouldNotLink, avoidSpellings):
    def testForm(form):
        #Find synsets of the form
        label = Label(form)

        #Not exact spelling
        for otherLabel in avoidSpellings:
            if label.sameSpelling(otherLabel): return None

        #Must link
        for i in range(1, len(shouldLink)):
            linkLabel = shouldLink[i]
            if not label.synonymous(linkLabel): return None

        #Must not link
        for i in range(0, len(shouldNotLink)):
            antiLinkLabel = shouldNotLink[i]
            if label.synonymous(antiLinkLabel): return None

        return label


    for synset in shouldLink[0].synsets:
        for word in synset.words():
            form = word.lemma()
            result = testForm(form)
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

class Label:
    def __init__(self,spelling):
        self.spelling = spelling
        self.synsets = set()
        self.forms = set()
        for word in wn.words(spelling):
            for synset in word.synsets(): self.synsets.add(synset)
            for form in word.forms(): self.forms.add(form)

    def __str__(self): return self.spelling

    def synonymous(self, that):
        return len(self.synsets.intersection(that.synsets))>0 #TODO: faster
    
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
    

for i in range(10000):
    word = random.choice(frequentNouns)
    chain = buildChain([Label(word)])
    if (len(chain)>=14): printChain(chain)
#printChain(buildChain([Label('hundred and one')]))

input('done')


#ISSUES:
#1. Tenuous links (is there a way to check sense frequency?)
#2. A-B-C links wordnet says A not linked to C when it seems so. (Maybe specify the nature of the link? e.g. "is a kind of")