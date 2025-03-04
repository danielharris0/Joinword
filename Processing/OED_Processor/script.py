#1. take OED
#2. remove 'abbr.' marked words
#3. add wordnet word variant forms (e.g. weave -> wove, weaving etc...)
from unidecode import unidecode
import re, wn

def getAlternateForms(spelling):
    forms = set([spelling])
    for word in wn.words(spelling): 
        for form in word.forms():
            forms.add(form.lower())
        for der in word.derived_words():
            for form in der.forms():
                forms.add(form.lower())
    return forms

wordlist = set()
i=0
for line in open('Processing/iweb_60000.txt','r',encoding='utf-8').readlines():
    if len(line)>3:
        word = line.lower().splitlines()[0].split('	')[2]
        i+=1
        if (i%100==0): print(i/30000)
        # = line.split('  ')

       # word = parts[0]
        #word = unidecode(word).lower()

        if not word.isalnum():
            continue

#if not word.isalpha():
       #     word = re.sub(r'[0-9]+', '', word)

       # partOfSpeech = parts[1].split(' ')[0].lower()

        #if partOfSpeech in ['abbr.','symb.']:
       #     continue

        wordlist.update(getAlternateForms(word))

file = open('Processing/OED_Processor/iweb_60000_Out.txt','w')
for word in wordlist:
    file.write(word+'\n')

print('done')