# Author: Akshit Arora
# Date Generated: June 13 2016, 9:06pm
# Script aims to look at the JSON file containing tweets by various politicians and the list of topics (lot.csv). And then determine whether the tweet is related to any of the topic or not. And then if the politician supports or oppose the policy.
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

def stem_tokens(tokens, stemmer):
	stemmed = []
	for item in tokens:
		stemmed.append(stemmer.stem(item))
	return stemmed

stemmer = PorterStemmer()

fo = open("output.txt","rb+")
foo = open("output1.txt","wb+") #cleaned tweets are put here
#foo2 = open("output3.txt","wb+") #testing whether the two lists are really being compared or not
foo3 = open("output4.txt","wb+") #final output
jsonLoaded = json.loads(fo.read())

for lastName,v in jsonLoaded.iteritems():
	for i in v:	
		punctuation = list(string.punctuation)
		#Cleaning the tweet.	
		i['text'] = re.sub(r"(?:\@|https?\://)\S+", "", i['text']) #for removing user mentions, hashtags and links in the tweets
		#removing stopwords because I do not want the key words that I search to be irrelevant
		i['text'] = i['text'].lower()
		terms_stop = [term for term in i['text'] if term not in punctuation]
		x='';
		for aktoken in terms_stop:
			x+=aktoken
		x = x.lstrip()
		
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
		tweet_tokenized2 = nltk.word_tokenize(x)
		

		###diagnosis
		#foo2.write('tweet_tokenized2:    ')
		#for val in tweet_tokenized2:
		#	foo2.write(val.encode('utf-8').strip()+' ')
		#diagnosis
		#foo2.write('\n\n')

		for line in fo2:
			a,b,c = line.split(',')
			if a.lower() == lastName.lower():	#opinion holder should be the same
				#b contains my topic and c contains the sub topic, combining them into one string
				b = b.lower()
				c = c.lower()
				b = b+' '+c
				#print b
				#b_tokenized = [i for i in x.split() if i not in stop and not punctuation] #sanitizing topic
				#by=''
				#for atoken in b_tokenized:
				#	by+=atoken+' '
				#by = by.lstrip()
				b_tokenized2 = nltk.word_tokenize(b)
				#print tweet_tokenized2
				#print b_tokenized2

				###diagnosis
				#foo2.write('b_tokenized2:    ')
				#for val in b_tokenized2:
				#	foo2.write(val.encode('utf-8').strip()+ ' ')
				#diagnosis
				#foo2.write('\n')

				for val in tweet_tokenized2:
					if val in b_tokenized2:
						if val not in {'government','and', 'campaign', 'free','policy', 'americans', 'american','wall', 'rights','states'}:
							#now we know that a part of topic/subtopic is present in the tweet text
							#this indicates that tweet is related to one of the topics in the topic list otherwise not
							print(lastName + '  '+val)
							foo3.write('"'+lastName.encode('utf-8').strip()+'", "'+b.encode('utf-8').strip()+'", "'+x.encode('utf-8').strip()+'"\n\n')
							continue
		fo2.close()
		#foo2.write('\n\n\n\n')
		#file closed
