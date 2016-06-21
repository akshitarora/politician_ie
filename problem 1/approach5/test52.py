# Author: Akshit Arora
# Date Generated: June 21 2016, 3:24pm
# Script aims to take clusters of tweets and treat them as documents for tf idf calculations. Then take the lot.txt file for topics and then run queries to determine which topic gives the highest tf-idf score and hence, gets associated to the cluster.
# Output expected <opinionHolder, document, topic, tf-idf> in output2.txt

import json
import io
import string
from nltk.stem.porter import *
from nltk import word_tokenize
from textblob import TextBlob as tb
import math
import nltk

def stem_tokens(tokens, stemmer):
	stemmed = []
	for item in tokens:
		stemmed.append(stemmer.stem(item))
	return stemmed

def tokenize(text):
	tokens = nltk.word_tokenize(text)
	stems = stem_tokens(tokens, stemmer)
	return stems

def tf(word, blob):
	return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
	return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
	return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
	return tf(word, blob) * idf(word, bloblist)

stemmer = PorterStemmer() #for stemming 
fo1 = io.open("output2.txt","w",encoding='utf8') #final output
fo = open("output1.txt","rb+")
jsonLoaded = json.loads(fo.read().decode('utf8', 'ignore')) #json object loaded 
fo.close()

for lastName,v in jsonLoaded.iteritems():
	myList = []
	myList2 = []
	for i1 in v:	
		myList.insert(-1,tb(i1['document']))
		myList2.insert(-1,i1['document'])
	bloblist = myList
	for i,blob in enumerate(bloblist):
		fo4 = open("lot.txt","r") #list of topics
		highest = 0.0
		highest_line = ''
		for line in fo4.readlines():
			line = line.decode('utf8', 'ignore')
			line = line.lower()
			#calculating tfidf
			topic_key = word_tokenize(line) #do not stem these, matching is affected
			topic_score = {word: tfidf(word,blob,bloblist) for word in topic_key}
			topic_sorted_words = sorted(topic_score.items(), key=lambda x: x[1], reverse=True)
			#I need to average the score in the above dictionary "topic_sorted_words"
			#print topic_sorted_words
			if sum(val for d,val in topic_sorted_words) > 0.0:
				print sum(val for d,val in topic_sorted_words)
			tfif = sum(val for d,val in topic_sorted_words) / len(topic_sorted_words)
			if tfif > highest: #assuming two scores never match, otherwise the first topic will be picked
				highest = tfif
				highest_line = line
		if highest > 0.0:
			print myList2[i]
			print '-----------------------------------------------------------------------------------------------------------------------'
			fo1.write('"'+lastName+'", "'+myList2[i]+'", "'+line+'", '+str(highest)+'\n')
	print '\n'
