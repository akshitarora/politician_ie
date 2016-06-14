# Author: Akshit Arora
# Date Generated: June 13 2016, 9:06pm
# Script aims to look at the JSON file containing tweets by various politicians and the list of topics (lot.csv). And then determine whether the tweet is related to any of the topic or not by comparing tokens of tweet and topic using the concept of tf-idf. Each tweet is treated as a document and then each topic is run as a query on the matrix. This script also includes the process of stemming.
#test run on Hillary Clinton (HillaryClinton), Cynthia McKinney (cynthiamckinney) and Gary Johnson (GovGaryJohnson)

import json
import pprint
import re
import nltk
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
from sklearn.feature_extraction.text import TfidfVectorizer

def stem_tokens(tokens, stemmer):
	stemmed = []
	for item in tokens:
		stemmed.append(stemmer.stem(item))
	return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems

punctuation = list(string.punctuation)
stemmer = PorterStemmer() #for stemming
token_dict = {} #defining token_dict
fo = open("output.txt","rb+")
foo = open("output1.txt","wb+") #cleaned tweets are put here
foo3 = open("output4.txt","wb+") #final output
jsonLoaded = json.loads(fo.read()) #json object loaded 
fo.close()

fo2 = open("output.txt","rb+")
jsonLoaded2 = json.loads(fo2.read())
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
	stri = 'this sentence but also king lord juliet'
	response = tfidf.transform(stri)
	print response
	tfs = tfidf.fit_transform(token_dict.values())
fo2.close()

print tfs
"""
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
