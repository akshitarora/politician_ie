# Author: Akshit Arora
# Date Generated: June 24 2016, 2:57pm
# Script aims to look at the page http://www.bbc.com/news/uk-politics-eu-referendum-36027205 This page contains structured information on various issues related to Brexit referendum 2016. It will read the file: "bbc.html" and generate triples from it. 

"""
For now I am taking UK Remain politician to be -> David Cameron (UK prime minister) 
And for UK leave -> Boris Johnson (former London Mayor)

Triples are of the kind:
<opinionHolder, remain/leave, broad_topic_debate, sub_topic>
"""

import nltk
import os
import io
import sys
import requests
import string
from nltk import word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

foo = io.open("output.txt","w",encoding='utf8') #final output
web = open("bbc.html","rb+") #webpage's HTML
punctuation = list(string.punctuation)
r = web.read()
#leave and remain lists
leavelist = ["Boris Johnson", "Liam Fox", "Zac Goldsmith", "Michael Gove", "Theresa Villiers", "John Whittingdale", "Priti Patel", "Chris Grayling", "Andrew R.T. Davies", "John Mann"]
remainlist = ["David Cameron", "Philip Hammond", "Jeremy Hunt", "Michael Fallon", "Sajid Javid", "Theresa May", "Patrick McLoughlin", "Nicky Morgan", "David Mundell", "George Osborne", "Liz Truss", "Alun Cairns", "Matthew Hancock", "Greg Hands", "Tina Stowell"]

soup = BeautifulSoup(r,'html5lib') #changed parser from html.parser to html5lib
for tr in soup.select("h3.eu-ref-issue__title"):
	#print tr.text
	issue = tr.text
	issue = issue.lower()
	issue = string.replace(issue, ' ','_')
	issue.lstrip()
	issue.rstrip()
	issue = 'article.eu-ref-issue--' + issue
	#print issue
	for article in soup.select(issue):
		a = article.select("h3.eu-ref-issue__title")[0].text
		b = article.select("div.eu-ref-issue__meta")[0]
		b = b.select("div.eu-ref-issue__description")[0].text
		a = a.lstrip()
		a = a.rstrip()
		b = b.lstrip()
		b = b.rstrip()
		b = b.rstrip('.')
		#basic topic keywords have been made, two types of subtopics exist (leave, remain)
		c = article.select("div.eu-ref-issue__summary--overview")[0].text
		c = string.replace(c,'\n',' ')
		c = string.replace(c,'\t',' ')
		c = string.replace(c,' ','_')
		c = string.replace(c,'_____________','')
		c = string.replace(c,'___________________________',' ')
		c =string.replace(c,'_____________________',' ')
		c =string.replace(c,'________',' ')
		c =string.replace(c,'_____',' ')
		c = string.replace(c,'_', ' ')
		#print a+' '+b+' '+c
		d = b+' '+c
		#clean d now, d = major_topic
		terms_stop = [term for term in d if term not in punctuation]
		x='';
		for aktoken in terms_stop:
			x+=aktoken
		x = x.lstrip()
		stop = stopwords.words('english')
		tweet_tokenized = [i for i in x.split() if i not in stop]
		x=''
		for aktoken in tweet_tokenized:
			x+=aktoken+' '
		d = x.lstrip()
		d = d.rstrip()
		d = a+' '+d
		#print d+'\n'
		leave = article.select("div.eu-ref-issue__summary--leave")[0]
		e = ''
		for li in leave.select("ul.eu-ref-issue__summary__policies"):
			li.text.rstrip()
			li.text.lstrip()
			e = e+' '+li.text
			e = e.lstrip()
			e = e.rstrip()
		e = string.replace(e,'\n',' ')
		e = string.replace(e, '                     ', ' ')
		for name in leavelist:
			foo.write('"'+name+'", "leave", "'+d+'", "'+e+'"\n\n')
			print '"'+name+'", "leave", "'+d+'", "'+e+'"\n\n'
		f = ''
		remain = article.select("div.eu-ref-issue__summary--remain")[0]
		for li in remain.select("ul.eu-ref-issue__summary__policies"):
			li.text.rstrip()
			li.text.lstrip()
			f = f+' '+li.text
			f = f.lstrip()
			f = f.rstrip()
		f = string.replace(f,'\n',' ')
		f = string.replace(f, '                     ', ' ')
		for name in remainlist:
			foo.write('"'+name+'", "remain", "'+d+'", "'+e+'"\n\n')
			print '"'+name+'", "remain", "'+d+'", "'+e+'"\n\n'
