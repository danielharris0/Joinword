import wn, random, homophoneDict, wn.similarity, copy

#Find the item linking to requiredLabel which also links to as many of the optionalLabels as possible. Yeild these in order
def FindMostLinked(requiredLabel, optionalLabels, avoid):
    words = []
    for word in requiredLabel.wordnetLinks: 
        if (not word in avoid):
            count = 0
            for label in optionalLabels:
                if word in label.wordnetLinks: count+=1
            words.append({'word':word, 'count':count})
    words.sort(key = lambda word: word['count'])

    for word in words: yield Label(word['word'])


class Label:
    def __init__(self, spelling):
        self.puzzleLinks = set() #All LEGAL links to other LABEL in the puzzle
        self.wordnetLinks = set() #All LEGAL links to any other WORD
        self.forms = set()
        self.spelling = spelling

        if spelling in homophoneDict.index: self.wordnetLinks.update(set(homophoneDict.index[spelling]))
        for word in wn.words(spelling):
            #Only include synsets for words of which 'spelling' is the canonical form (otherwise Label('caught') will include the synsets for 'catch', including synonyms like 'hitch', 'exception' etc.)
            if spelling == word.lemma():
                for synset in word.synsets():
                    for synonym in synset.words():
                        self.wordnetLinks.add(synonym.lemma())
                    for hypernym in synset.hypernyms():
                        for lemma in hypernym.lemmas(): self.wordnetLinks.add(lemma)
                    for hyponym in synset.hyponyms():
                        for lemma in hyponym.lemmas(): self.wordnetLinks.add(lemma)                 
            for form in word.forms(): self.forms.add(form)


    def __str__(self): return self.spelling
    def __repr__(self): return self.spelling

    def AddToPuzzleL(self, puzzle):
        puzzle.left.append(self)
        for label in puzzle.right:
            if label.spelling in self.wordnetLinks:
                self.puzzleLinks.add(label)
                label.puzzleLinks.add(self)

    def AddToPuzzleR(self, puzzle):
        puzzle.right.append(self)
        for label in puzzle.left:
            if label.spelling in self.wordnetLinks:
                self.puzzleLinks.add(label)
                label.puzzleLinks.add(self)

    def RemoveFromPuzzleL(self, puzzle):
        puzzle.left.remove(self)
        for label in puzzle.right:
            if self in label.puzzleLinks: label.puzzleLinks.remove(self)
            if label in self.puzzleLinks: self.puzzleLinks.remove(label)

    def RemoveFromPuzzleR(self, puzzle):
        puzzle.right.remove(self)
        for label in puzzle.left:
            if self in label.puzzleLinks: label.puzzleLinks.remove(self)
            if label in self.puzzleLinks: self.puzzleLinks.remove(label)

class Puzzle:

    def __init__(self, l, r):

        self.left = []
        self.right = []

        #The solution links left[i] <--> right[i]
        #We also always have decoy links left[i] <-> right[i-1] in a zig-zag
        Label(l).AddToPuzzleL(self)
        Label(r).AddToPuzzleR(self)

    def print(self):
        print("\nPuzzle:")
        for i in range(max(len(self.left), len(self.right))):
            line = str(i+1) + ': '
            if i < len(self.left):
                line += self.left[i].spelling + '('
                for j in range(len(self.left[i].puzzleLinks)):
                    line += str(self.right.index(list(self.left[i].puzzleLinks)[j])+1)
                    if j < len(self.left[i].puzzleLinks)-1: line += ", "
                line+=")"
            line += (30 - len(line)) * ' '
            if i < len(self.right):
                line += self.right[i].spelling + '('
                for j in range(len(self.right[i].puzzleLinks)):
                    line += str(self.left.index(list(self.right[i].puzzleLinks)[j])+1)
                    if j < len(self.right[i].puzzleLinks)-1: line += ", "
                line+=")"
            print(line)
        
    #Add a label to left and to right
    def expand(self):
        #Find a L and R s.t. links(L,R) and any links with existing labels do not add additional solutions. (Nb. this is a sufficient but not neccesary condition for construction a good puzzle).
        #In fact, MAXIMISE the number of 'decoy links'
        
        #Repeat:
            # Find the word L' which links to the the latest R, and as many other Rs as possible
            # From all possible links to that word L', find the one R' which links to as many other Ls as possible
            # Test: For each of L's links other than to R', are any of them valid solutions? If so - pick again

        def IsExpansionGood():
            for label in newL.puzzleLinks:
                if label!=newR and self.LinkIsValidSolution(newL, label):
                    return False
            return True
        
        allSpellings = set()
        for l in self.left: allSpellings.update(l.forms)
        for r in self.right: allSpellings.update(r.forms)

        for newL in FindMostLinked(self.right[-1], self.right,allSpellings):
            newAllSpellings = allSpellings.union(newL.forms)
            for newR in FindMostLinked(newL, self.left, newAllSpellings):
                newL.AddToPuzzleL(self); newR.AddToPuzzleR(self)
                if IsExpansionGood():
                    self.print()
                    response = input('good?')
                    if response =='y':
                        return False
                    elif response == 'nn':
                        return True
                    elif response == 's':
                        newL.RemoveFromPuzzleL(self); newR.RemoveFromPuzzleR(self)
                        break
                newL.RemoveFromPuzzleL(self); newR.RemoveFromPuzzleR(self)

        print("No good way to expand.")

                

    def LinkIsValidSolution(self, l, r):
        linksL = {}
        for item in self.left:
            linksL[item] = []
            for link in item.puzzleLinks: linksL[item].append(link)
        linksR = {}
        for item in self.right:
            linksR[item] = []
            for link in item.puzzleLinks: linksR[item].append(link)

        valid = True 

        def selectLink(l,r):
            #Remove all other connected links
            if l in linksL:
                for label in linksL[l]:
                    if label!=r: removeLinkR(l, label)

            if r in linksR:
                for label in linksR[r]:
                    if label!=l: removeLinkL(label,r)
            
        def removeLinkR(l,r):
            nonlocal valid
            if r in linksR and l in linksR[r]:
                linksR[r].remove(l)
                if len(linksR[r])==0: valid=False  
                if len(linksR[r])==1: selectLink(linksR[r][0], r)

        def removeLinkL(l,r):
            nonlocal valid
            if l in linksL and r in linksL[l]:
                linksL[l].remove(r)
                if len(linksL[l])==0: valid=False  
                if len(linksL[l])==1: selectLink(linksL[l][0], l)

        selectLink(l,r)
        return valid     

puzzle = Puzzle('bucket','pail')
savepoints = []

while True:
    backtrack = puzzle.expand()
    if backtrack:
        puzzle = copy.deepcopy(savepoints.pop())
    else:
        savepoints.append(copy.deepcopy(puzzle))

