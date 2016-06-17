# Author: Akshit Arora
# Date Generated: June 13 2016, 9:06pm
# Script aims to look at the JSON file containing tweets by various politicians and the list of topics (lot.csv). And then determine whether the tweet is related to any of the topic or not by comparing tokens of tweet and topic using the concept of tf-idf. Each tweet is treated as a document and then each topic is run as a query on the matrix. This script also includes the process of stemming.
#test run on Hillary Clinton (HillaryClinton), Cynthia McKinney (cynthiamckinney) and Gary Johnson (GovGaryJohnson)

# June 13 2016: tried http://www.cs.duke.edu/courses/spring14/compsci290/assignments/lab02.html 
# June 15 2016: trying http://stevenloria.com/finding-important-words-in-a-document-using-tf-idf/
# June 16 2016: all unicode errors got resolved https://gist.github.com/sloria/6407257 

from __future__ import division, unicode_literals
import json
import pprint
import re
import nltk
import sys 
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
import scrapy
import requests
import libxml2
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
from nltk.corpus import stopwords
from nltk.stem.porter import *
import os
import math
from textblob import TextBlob as tb
import io

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


punctuation = list(string.punctuation)
stemmer = PorterStemmer() #for stemming
fo = open("output.txt","rb+")
foo3 = io.open("output6.txt","w",encoding='utf8') #final output
jsonLoaded = json.loads(fo.read().decode('utf8', 'ignore')) #json object loaded 
fo.close()

#fo2 = open("output.txt","rb+")
#jsonLoaded2 = json.loads(fo2.read())

for lastName,v in jsonLoaded.iteritems():
	myList = []
	myList2 = []
	for i in v:
		i['text'] = i['text'].lower()
		i['text'] = re.sub(r"(?:\@|https?\://)\S+", "", i['text'])
		i['text'] = string.replace(i['text'], u'\u2026', ' ')
		i['text'] = string.replace(i['text'], u'\u2019', ' ')
		i['text'] = string.replace(i['text'], u'\u201c', ' ')
		i['text'] = string.replace(i['text'], u'\u201d', ' ')
		i['text'] = string.replace(i['text'], u'\u200a', ' ')
		i['text'] = string.replace(i['text'],u'\u2014',' ')
		i['text'] = string.replace(i['text'],u'\u2192',' ')
		myList2.append(i['text'])
		terms_stop = [term for term in i['text'] if term not in punctuation]
		x='';
		#stemming:
		terms_stop = stem_tokens(terms_stop, stemmer)
		#concatenation of tokens
		for aktoken in terms_stop:
			x+=aktoken
		x = x.lstrip()
		stop = stopwords.words('english')
		tweet_tokenized = [i for i in x.split() if i not in stop and not term.startswith(('#', '@'))]
		x=''
		#concatenation of tokens
		for aktoken in tweet_tokenized:
			x+=aktoken+' '
		x = x.lstrip()
		#tweet has been cleaned
		if x:	#sometimes tweets end up empty after all cleaning. this problem makes denominator of tf function = 0, and hence we get a 'divide by zero' error. So we need this check
			myList.insert(-1,tb(x))
	#print myList #this is my bloblist
	bloblist = myList
	for i,blob in enumerate(bloblist):
		#calculating scores:
		#scores = {word: tfidf(word,blob,bloblist) for word in blob.words}
		#sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
		fo4 = open("lot.txt","r") #list of topics
		for line in fo4.readlines():
			line = line.decode('utf8', 'ignore')
			line = line.lower()
			topic_key = word_tokenize(line) #do not stem these, matching is affected
			topic_score = {word: tfidf(word,blob,bloblist) for word in topic_key}
			topic_sorted_words = sorted(topic_score.items(), key=lambda x: x[1], reverse=True)
			for word, score in topic_sorted_words[:3]:
				if score > 1.0:
					#print '\n'
					#print topic_key
					#print '  :  '
					#print myList2[i]
					#print("Word: {}, TF-IDF: {}".format(word, round(score, 5)))
					#print '\n'
					#print lastName
					#print line
					print str(round(score,5))
					#print myList2[i]
					foo3.write('"'+lastName+'", "'+line+'", "'+word+'", '+str(round(score, 5)).strip()+', "'+myList2[i]+'"')
					foo3.write('\n')
					continue
				#print '\n'
			
		fo4.close()
	#following code runs perfectly!
	"""
	for i, blob in enumerate(bloblist):
		print("Top words in document {}".format(i + 1))
		scores = {word: tfidf(word,blob,bloblist) for word in blob.words}		
		sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
		for word, score in sorted_words[:3]:
			print("Word: {}, TF-IDF: {}".format(word, round(score, 5)))
		print '\n\n\n'
	"""

"""
# June 13: http://www.cs.duke.edu/courses/spring14/compsci290/assignments/lab02.html try. Only the following code works, stri input doesnt work!
token_dict = {} #defining token_dict
for lastName,v in jsonLoaded.iteritems():
	k = 0
	for i in v:
		lowers = i['text'].lower()
		terms_stop = [term for term in i['text'] if term not in punctuation]
		x='';
		#stemming:
		terms_stop = stem_tokens(terms_stop, stemmer)
		#concatenation of tokens
		for aktoken in terms_stop:
			x+=aktoken
		x = x.lstrip()
		k=k+1 #because i is unhashable dict
		token_dict[lastName,k] = x
	tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
	#stri = 'this sentence but also king lord juliet'
	#response = tfidf.transform(stri)
	#print response
	tfs = tfidf.fit_transform(token_dict.values())
fo2.close()

print tfs
"""
"""

#The following approach is for comparing two token lists (tweet's and topic's)

for lastName,v in jsonLoaded.iteritems():
	for i in v:	
		#Cleaning the tweet.	
		i['text'] = re.sub(r"(?:\@|https?\://)\S+", "", i['text']) #for removing user mentions, hashtags and links in the tweets
		#removing stopwords because I do not want the key words that I search to be irrelevant
		i['text'] = i['text'].lower()
		terms_stop = [term for term in i['text'] if term not in punctuation]
		x='';
		#stemming:
		terms_stop = stem_tokens(terms_stop, stemmer)
		#concatenation of tokens
		for aktoken in terms_stop:
			x+=aktoken
		x = x.lstrip()
		#further cleaning
		stop = stopwords.words('english')
		tweet_tokenized = [i for i in x.split() if i not in stop and not term.startswith(('#', '@'))]
		#print tweet_tokenized
		x=''
		for aktoken in tweet_tokenized:
			x+=aktoken+' '
		x = x.lstrip()
		#tweet has been sanitized and is ready to be compared with list of topics mentioned
		foo.write(lastName+':  ')
		foo.write('" '+x.encode('utf-8').strip()+' "')
		foo.write('\n\n')
		fo2 = open("lot.csv","rb+")
		tweet_tokenized2 = tokenize(x)
		
		for line in fo2:
			a,b,c = line.split(',')
			#IF opinion holder is the same
			if a.lower() == lastName.lower():	
				#b contains my topic and c contains the sub topic, combining them into one string
				b = b.lower()
				c = c.lower()
				b = b+' '+c
				b_tokenized2 = tokenize(b)
				for val in tweet_tokenized2:
					if val in b_tokenized2:
						if val not in {'government','and', 'campaign', 'free','policy', 'americans', 'american','wall', 'rights','states'}:
							#now we know that a part of topic/subtopic is present in the tweet text
							#this indicates that tweet is related to one of the topics in the topic list otherwise not
							print(lastName + '  '+val)
							foo3.write('"'+lastName.encode('utf-8').strip()+'", "'+b.encode('utf-8').strip()+'", "'+x.encode('utf-8').strip()+'"\n\n')
							continue
		fo2.close()
"""
