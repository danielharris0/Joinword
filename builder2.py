import wn, homophoneDict, random, csv
from queue import Queue 

#start with a few 3+ relation synonyms / homophones / hypernyms

class Word: #(as in, like, a string)
    def __init__(self, spelling):
        self.spelling = spelling
        self.children = None

    def __str__(self): return self.spelling
    def __repr__(self): return "{word: " + self.spelling + "}"

    def Children(self):
        if self.children!=None: return self.children

        self.children = []
        if self.spelling in homophoneDict.index:
            self.children += homophoneDict.index[self.spelling]

        for word in wn.words(self.spelling):
            for synset in word.synsets():
                self.children += synset.lemmas()
                for hypernym in synset.hypernyms():
                    self.children += hypernym.lemmas()
                for hyponym in synset.hyponyms():
                    self.children += hyponym.lemmas()
        self.children = set(self.children)

        return self.children


def Join_Words_And_Print_Path(a, b):

    def BFS_Join_Words(a, b):
        seen = set([a.spelling])
        frontier = Queue(); frontier.put(a) 
        path = {}
        count = 0
        while count < 1000000:
            count += 1
            word = frontier.get()
            for child in word.Children():
                if not child in seen:
                    seen.add(child)
                    child = Word(child)
                    path[child] = word
                    if (child.spelling == b.spelling): yield (child, path)
                    frontier.put(child)

    def PrintPath(end, path):
        print("\nPath:")
        while end in path:
            print(end)
            end = path[end]
        input(end)

    for (end, path) in BFS_Join_Words(Word(a), Word(b)):
        PrintPath(end, path)


def RandomWord():
    file = open('frequentNouns.csv','r')
    return Word(random.choice(file.readlines()).strip('\n'))

def BuildLinear(a):
    start = RandomWord()
    if a!=None: start = a
    chain = [start]

    while True:
        options = chain[-1].Children()
        for i in range(len(chain)):
            if i%2 == 1-(len(chain)%2) and i < len(chain)-1:
                options.difference_update(chain[i].Children())
        
        options = list(options)
        random.shuffle(options)

        for word in options:

            for i in range(0, len(chain), 2):
                print(chain[i].spelling, end=' ' * (20 - len(chain[i].spelling)))
            if len(chain)%2==0: print(word, end = '')
            print()
            for i in range(1, len(chain), 2):
                print(chain[i].spelling, end=' ' * (20 - len(chain[i].spelling)))
            if len(chain)%2==1: print(word, end = '')
            response = input('\n---')
            if response=='y':
                chain.append(Word(word))
                break
            if response=='b':
                chain.pop()
                break
            elif response!='':
                chain.append(Word(response))
                break


BuildLinear(Word('comet'))
#Join_Words_And_Print_Path('snowball','cupid')