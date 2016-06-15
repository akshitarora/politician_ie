# Author: Akshit Arora
# Date Generated: June 14 2016, 9:43pm
# Script aims to look at the HTML of http://2016election.procon.org/view.source-summary-chart.php This page contains structured information on political opinions of popular candidates (Hillary Clinton, Bernie Sanders, Donald Trump, Gary Johnson, Jill Stein) in the 2016 US Presidential race. It will read the file: "webpage_HTML" and generate triples from it. 

"""
Now how to deal with the tabular values:
Pro -> 1 triple indicating Support with timestamp=0
Con -> 1 triple indicating Oppose with timestamp=0
Now Con -> 2 triples {1st triple indicating Pro with 0 timestamp} {2nd triple indicating Con with 1 as timestamp}
Now Pro -> 2 triples {1st triple indicating Con with 0 timestamp} {2nd triple indicating Pro with 1 as timestamp}
NC: not clearly pro/con. This will tagged as Neutral response and 1 triple
Now NC -> same as NC
? -> no triple generated <it indicates: None Found>
"""

import nltk
import os
import sys
import requests
import string
from nltk import word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

http_proxy  = "http://anz148198:07h5AK79bL@10.10.78.61:3128"
https_proxy = "https://anz148198:07h5AK79bL@10.10.78.61:3128"
foo = open("output.txt","wb+") #triples put here
web = open("webpage_HTML","rb+") #webpage's HTML
punctuation = list(string.punctuation)

r = web.read()
#r2 = requests.get('http://2016election.procon.org/view.source-summary-chart.php',proxies={"http":http_proxy,"https":https_proxy})
soup = BeautifulSoup(r,'html5lib') #changed parser from html.parser to html5lib
for tr in soup.select("table.summary-chart tr"):
	if tr.select("div.question-issue") == []: #to avoid empty rows in between
		continue

	a_issue = ''
	for issue in tr.select("div.question-issue"):
		a_issue = issue.text
	#print a_issue
	b_issue = ''
	for issue2 in tr.select("div.question-question"):
		b_issue = issue2.text

	#cleaning the b_issue = question
	b_issue = b_issue.lower()
	a_issue = a_issue.lower()
	terms_stop = [term for term in b_issue if term not in punctuation]
	x='';
	for aktoken in terms_stop:
		x+=aktoken
	x = x.lstrip()
	stop = stopwords.words('english')
	tweet_tokenized = [i for i in x.split() if i not in stop]
	x=''
	for aktoken in tweet_tokenized:
		x+=aktoken+' '
	b_issue = x.lstrip()
	b_issue = b_issue.rstrip()
	#storing final keywords in Issue
	Issue = a_issue + ' ' + b_issue
	#print Issue
	i=0
	for response in tr.select("td.question-response"):
		i=i+1
		if i==1:
			oh = 'Hillary Clinton'
		elif i==2:
			oh = 'Bernie Sanders'
		elif i==3:
			oh = 'Donald Trump'
		elif i==4:
			oh = 'Gary Johnson'
		else:
			oh = 'Jill Stein'
		#print oh
		response2 = response.text
		if(response2.lower() == '?'):
			continue
		if response2.lower() == 'pro':
			opinion = 'support'
			print '"'+oh+'", "'+opinion+'", "'+Issue+'", 0'
			foo.write('"'+oh+'", "'+opinion+'", "'+Issue+'", 0')
		elif response2.lower() == 'now pro':
			opinion = 'oppose'
			print '"'+oh+'", "'+opinion+'", "'+Issue+'", 0'
			foo.write('"'+oh+'", "'+opinion+'", "'+Issue+'", 0')
			foo.write('\n')
			opinion = 'support'
			print '"'+oh+'", "'+opinion+'", "'+Issue+'", 1'
			foo.write('"'+oh+'", "'+opinion+'", "'+Issue+'", 1')
		elif response2.lower() == 'con':
			opinion = 'oppose'
			print '"'+oh+'", "'+opinion+'", "'+Issue+'", 0'
			foo.write('"'+oh+'", "'+opinion+'", "'+Issue+'", 0')
		elif response2.lower() == 'now con':
			opinion = 'support'
			print '"'+oh+'", "'+opinion+'", "'+Issue+'", 0'
			foo.write('"'+oh+'", "'+opinion+'", "'+Issue+'", 0')
			foo.write('\n')
			opinion = 'oppose'
			print '"'+oh+'", "'+opinion+'", "'+Issue+'", 1'
			foo.write('"'+oh+'", "'+opinion+'", "'+Issue+'", 1')
		elif response2.lower() == 'nc' or response2.lower() == 'now nc':
			opinion = 'neutral'
			print '"'+oh+'", "'+opinion+'", "'+Issue+'", 0'
			foo.write('"'+oh+'", "'+opinion+'", "'+Issue+'", 0')
		foo.write('\n')
