import re, string

def remove_stops(iterator, stopwords):
    filtered_words = []
    for word in g:
        word = str(word) 
        filtered_w = re.sub('[%s]' % re.escape(string.punctuation), '', word)
        if out not in stopwords:
            important_words.append(filtered_w) 
    return filtered_words                

