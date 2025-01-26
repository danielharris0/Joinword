import random

def isDisordered(perm):
    for i in range(len(perm)):
        if perm[i]==i: return False
    return True
    
def applyPermutationToPuzzle(left, right, answers, a = None, b = None):
    #answers is a list matching left indices to right indices -- answers[i] gives a list of the indices of the items in 'right' to which the ith item of 'left' can be linked
    l = len(left)

    def badShuffleL(a):
        if a[0]==0: return True #don't want the 'end' of the chain to be the first node you see
        return False
    
    def badShuffleR(a,b):
        if b[0]==len(right)-1: return True #don't want the 'end' of the chain to be the first node you see
        for i in range(l):
            pairL = a[i]
            pairR = b[i]
            if pairL==pairR: return True #don't want the 'actual' answer to be so obvious
        return False

    if a==None:
        a = list(range(l))  #left[a[i]] goes in the ith position in the final puzzle listing; a[i] gives the index in 'left' of the ith position in the final puzzle listing
        while (badShuffleL(a)): random.shuffle(a)

    if b==None:
        b = list(range(l))  #right[b[i]] goes in the ith position in the final puzzle listing; b[i] gives the index in 'right' of the ith position in the final puzzle listing
        while (badShuffleR(a,b)): random.shuffle(b)

    s = "new Puzzle(["
    for i in range(l): s+='\''+left[a[i]]+'\''+','
    s=s[:-1]+'],['
    for i in range(l): s+='\''+right[b[i]]+'\''+','
    s=s[:-1]+'],['
    for i in range(l):
        s += '['
        leftIndex = a[i]
        
        for j in answers[leftIndex]:
            puzzleIndexRight = None
            for k in range(l):
                if b[k]==j: puzzleIndexRight = k
            s += str(puzzleIndexRight+1) + ','
        s = s[:-1]
        s+='],'

    s=s[:-1]+']),'

    #print()
    #print(s) 
    return (s,a,b)

def applyPermutationToRusianDoll(left, right):
    answers = [[j for j in range(i,len(left))] for i in range(len(left))]
    print(answers)
    applyPermutationToPuzzle(left, right, answers)
    
def generatePuzzleListingFromChain(chain, a=None, b=None):
    print('\n')
    print(chain)

    print()
    for i in range(0,len(chain),2):
        if i>0: print(chain[i] + chain[i-1], end="  ")
        print(chain[i] + chain[i+1], end="  ")
    print()

    print(a)

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

    print(permutation)

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

    input(s)

#applyPermutationToRusianDoll([],[])
#generatePuzzleListingFromChain(['0','1','2','3','4','5','6','7','8','9'], [2,1,0,3,4])

#chainLength = puzzleSize * 2
#while True:
#    (result, c) = growChain([],chainLength)
#    generatePuzzleListingFromChain(c[:chainLength])