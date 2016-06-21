# Author: Akshit Arora
# Date Generated: June 21 2016, 1:45pm
# Script aims to cluster the tweets, given the number of tweets per cluster. Tweet cleaned. Again a JSON object is obtained as an output

import json
import io
import os
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
import re
from nltk.stem.porter import *

def stem_tokens(tokens, stemmer):
	stemmed = []
	for item in tokens:
		stemmed.append(stemmer.stem(item))
	return stemmed

#stop = stopwords.words('english')
stemmer = PorterStemmer() #for stemming
punctuation = list(string.punctuation)
fo1 = io.open("output1.txt","wb") #final output
fo = open("output.txt","rb+")
jsonLoaded = json.loads(fo.read().decode('utf8', 'ignore')) #json object loaded 
fo.close()

tweets_per_cluster = 5
tweets_per_person = 200

fo1.write('{')
for lastName,v in jsonLoaded.iteritems():
	#print type(v)
	o = 0
	fo1.write('"'+lastName+'": [')
	for p in [v[i:i+tweets_per_cluster] for i in xrange(0, tweets_per_person, tweets_per_cluster)]:
		o=o+1
		fo1.write('{ "document" : "')
		for t in p:
			print '------------------------------------------------------------------------'
			#removing URLs from tweet text
			split_text = t['text'].split()
			for a in t['text'].split():
				if a.startswith('https://'):
					split_text.remove(a)
			t['text'] = " ".join(split_text)
			print t['text']
			t['text'] = t['text'].lower()
			terms_stop = [term for term in t['text'] if term not in punctuation]
			x='';
			#stemming:
			terms_stop = stem_tokens(terms_stop, stemmer)
			#concatenation of tokens
			for aktoken in terms_stop:
				if aktoken != '\n':
					x+=aktoken
			x = x.lstrip()
			#print x
			#tweet_tokenized = [it for it in x.split() if it not in term.startswith(('#', '@'))]
			#concatenation of tokens
			#for aktoken in tweet_tokenized:
			#	x+=aktoken+' '
			#x = x.lstrip()
			#tweet has been cleaned
			t['text'] = x
			fo1.write(t['text'].encode('utf8').strip()+'  ')
		#print p[1]['text'] + ' -NEXT- ' + p[2]['text'] + ' -NEXT- ' + p[3]['text'] + ' -NEXT- ' + p[4]['text']+ ' -NEXT- ' + p[0]['text']
		#print '------------------document over--------------------------------------------------------------------------------------------'
		fo1.write('" },')
		#fo1.write('{ "document" : "'+p[0]['text'].encode('utf8').strip()+'  '+p[1]['text'].encode('utf8').strip()+'  '+p[2]['text'].encode('utf8').strip()+'  '+p[3]['text'].encode('utf8').strip()+'  '+p[4]['text'].encode('utf8').strip()+'" },')
	#print '\n\n\n\n'
	fo1.close()
	with open("output1.txt", 'rb+') as filehandle:
		filehandle.seek(-1, os.SEEK_END)
		filehandle.truncate()
	fo1 = io.open("output1.txt","ab")
	fo1.write('],')
fo1.close()
with open("output1.txt", 'rb+') as filehandle:
	filehandle.seek(-1, os.SEEK_END)
	filehandle.truncate()
fo1 = io.open("output1.txt","ab")
fo1.write('}')
fo1.close()
