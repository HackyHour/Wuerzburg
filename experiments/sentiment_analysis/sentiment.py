#!/usr/bin/env python3
# Derived from https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/ and following parts by Marco Bonzanini (http://marcobonzanini.com/) (licensed under a Creative Commons Attribution 4.0 International License (http://creativecommons.org/licenses/by/4.0/))
from nltk.tokenize import word_tokenize
from collections import defaultdict
from nltk.corpus import stopwords
from collections import Counter
from nltk import bigrams 
import operator 
import string
import json
import nltk
import math
import re
 
fname = 'trump.json'
nltk.download('stopwords')
com = defaultdict(lambda : defaultdict(int))
 
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens
 
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via', 'amp', '…', '’', '“']

n_docs = 0
with open(fname, 'r') as f:
    n_docs = n_docs + 1
    count_all = Counter()
    for line in f:
        tweet = json.loads(line)
        # Create a list with all the terms
        #terms_all = [term for term in preprocess(tweet['text'])]
        terms_all = [term for term in preprocess(tweet['text'], True) if term not in stop]
        terms_single = set(terms_all)
        # Count hashtags only
        terms_hash = [term for term in preprocess(tweet['text']) 
              if term.startswith('#')]
# Count terms only (no hashtags, no mentions)
        terms_only = [term for term in preprocess(tweet['text'], True) 
              if term not in stop and
              not term.startswith(('#', '@'))] 
              # mind the ((double brackets))
              # startswith() takes a tuple (not a list) if 
              # we pass a list of inputs
        # Update the counter
        count_all.update(terms_single)
        for i in range(len(terms_only)-1):            
            for j in range(i+1, len(terms_only)):
                w1, w2 = sorted([terms_only[i], terms_only[j]])                
                if w1 != w2:
                    com[w1][w2] += 1
    # Print the most frequent words
    print("Most common words:")
    print(count_all.most_common(10))
    print()
 
com_max = []
# For each term, look for the most common co-occurrent terms
for t1 in com:
    t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
    for t2, t2_count in t1_max_terms:
        com_max.append(((t1, t2), t2_count))
# Get the most frequent co-occurrences
terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
print("Most common co-occurences:")
print(terms_max[:10])
print()

# n_docs is the total n. of tweets
p_t = {}
p_t_com = defaultdict(lambda : defaultdict(int))
 
for term, n in count_all.items():
    p_t[term] = n / n_docs
    for t2 in com[term]:
        p_t_com[term][t2] = com[term][t2] / n_docs

positive_vocab = [
    'good', 'nice', 'great', 'awesome', 'outstanding',
    'fantastic', 'terrific', ':)', ':-)', 'like', 'love',
    # shall we also include game-specific terms?
    # 'triumph', 'triumphal', 'triumphant', 'victory', etc.
]
negative_vocab = [
    'bad', 'terrible', 'crap', 'useless', 'hate', ':(', ':-(',
    # 'defeat', etc.
]

pmi = defaultdict(lambda : defaultdict(int))
for t1 in p_t:
    for t2 in com[t1]:
        denom = p_t[t1] * p_t[t2]
        pmi[t1][t2] = math.log2(p_t_com[t1][t2] / denom)
 
semantic_orientation = {}
for term, n in p_t.items():
    positive_assoc = sum(pmi[term][tx] for tx in positive_vocab)
    negative_assoc = sum(pmi[term][tx] for tx in negative_vocab)
    semantic_orientation[term] = positive_assoc - negative_assoc

semantic_sorted = sorted(semantic_orientation.items(), 
                         key=operator.itemgetter(1), 
                         reverse=True)
top_pos = semantic_sorted[:10]
top_neg = semantic_sorted[-10:]
 
print("Most positive words:")
print(top_pos)
print()
print("Most negative words:")
print(top_neg)
print()

print("Semantic orientation of some specific words")
print("wall: %f" % semantic_orientation['wall'])
print("canada: %f" % semantic_orientation['canada'])
print("mexican: %f" % semantic_orientation['mexican'])
print("guns: %f" % semantic_orientation['guns'])
print("free: %f" % semantic_orientation['free'])

#for key, value in semantic_orientation.items():
#    if not value == 0:
#        print("{}: {}".format(key, value))
