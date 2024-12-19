import wn, homophoneDict, random
from queue import Queue 

#start with a few 3+ relation synonyms / homophones / hypernyms

class Word: #(as in, like, a string)
    def __init__(self, spelling):
        self.spelling = spelling

    def __str__(self): return self.spelling
    def __repr__(self): return "[word: " + self.spelling + "]"

    def Children(self):
        if self.spelling in homophoneDict.index:
            for spelling in homophoneDict.index[self.spelling]: yield Word(spelling)

        for word in wn.words(self.spelling):
            for synset in word.synsets():
                for lemma in synset.lemmas(): yield Word(lemma)
                for hypernym in synset.hypernyms():
                    for lemma in hypernym.lemmas(): yield Word(lemma)
                for hyponym in synset.hyponyms():
                    for lemma in hyponym.lemmas(): yield Word(lemma)

def BFS_Join_Words(a, b):
    seen = set([a.spelling])
    frontier = Queue(); frontier.put(a) 
    path = {}
    count = 0
    while count < 1000000:
        count += 1
        word = frontier.get()
        for child in word.Children():
            if not child.spelling in seen:
                seen.add(child.spelling)
                path[child] = word
                if (child.spelling == b.spelling): yield (child, path)
                frontier.put(child)

def PrintPath(end, path):
    print("\nPath:")
    while end in path:
        print(end)
        end = path[end]
    input(end)

for (end, path) in BFS_Join_Words(Word('see'), Word('sea')):
    PrintPath(end, path)