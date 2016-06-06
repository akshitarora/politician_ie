# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from bs4 import BeautifulSoup
import sys
import lxml
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

outfile = open("htmltotext.txt", mode='w')
orig_stdout = sys.stdout
sys.stdout = outfile

redditstopwords = ['permalinkembed', 'save', 'gold', 'reply', 'parent', 'days', 'hours', 'permalink', 'embed', 'parent', 'give', 'report', 'reddit', 'points', 'ago', 'load', 'more', 'comments', '[deleted]', '[removed]', 'submissions', 'subreddit']

htmlfile = open("ucla.htm", errors = 'ignore').read()

soup = BeautifulSoup(htmlfile, 'lxml')

for scr in soup(["script", "style"]):
    scr.extract()

text = soup.get_text()
print(text)
#tokens = word_tokenize(text)
#tokenlist = []
#
#for word in tokens: 
#    word = word.lower() 
#    if word.isalpha():
#        tokenlist.append(word) 
#
#filtered_tokens = [word for word in tokenlist if word not in stopwords.words('english') and word not in redditstopwords]
#freq1 = nltk.FreqDist(filtered_tokens)
#
#for token in freq1:
#    if freq1[token]>5:
#        print(token, ":", freq1[token])

sys.stdout = orig_stdout