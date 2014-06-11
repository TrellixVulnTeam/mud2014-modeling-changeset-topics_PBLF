import re, string

def openf(fname):
    unfiltered = [] 
    with open(fname, 'r') as f:
        for line in f:
            line = line.strip().split() 
            for word in line:
                unfiltered.append(word) 
    return unfiltered


def generator(lyst): 
    for word in lyst:
        yield word 

def remove_stops(g):
    stopwords = ['and','the']
    important_words = []
    for word in g:
        c = str(word) 
        out = re.sub('[%s]' % re.escape(string.punctuation), '', c)
        if out not in stopwords:
            important_words.append(out) 
    return important_words                


def main(): 
    unfilter_w = openf('txt.txt') 
    g = generator(unfilter_w) 
    print(remove_stops(g)) 

main()
