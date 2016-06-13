# Author: Akshit Arora
# Date Generated: Fri Jun 3 2016 11:49AM
# Script aims to take the JSON file containing tweets of various politicians. Clean the tweets. Search them on google news website. Collect the first news article retrieved relevant to the tweet. Clean that HTML page of the article and retrieve plain text. Store this text in JSON format along with the tweet.

import json
import pprint
import re
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
import scrapy
import requests
import libxml2
#from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def clean_(st):
	if st.startswith("/url?q="):
		strin = st[7:]
		a,b = strin.split('&sa=')
		return a	

fo = open("output.txt","rb+")
#foo = open("output1.txt","wb+")
foo = open("output2.txt","wb+")

jsonLoaded = json.loads(fo.read())

#jsonLoaded is a dictionary now
#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(jsonLoaded['clinton'][0])		#testing
#type(jsonLoaded)

http_proxy  = "http://anz148198:07h5AK79bL@10.10.78.61:3128"
https_proxy = "https://anz148198:07h5AK79bL@10.10.78.61:3128"


for lastName,v in jsonLoaded.iteritems():
	for i in v:	
		punctuation = list(string.punctuation)
		#Cleaning the tweet.	
		i['text'] = re.sub(r"(?:\@|https?\://)\S+", "", i['text']) #for removing user mentions, hashtags and links in the tweets
		#removing stopwords because I do not want the key words that I search to be irrelevant
		i['text'] = i['text'].lower()
		terms_stop = [term for term in i['text'] if term not in punctuation and not term.startswith(('#', '@'))]
		x='';
		for aktoken in terms_stop:
			x+=aktoken
		x = x.lstrip()
		#tweet has been sanitized and is ready to be searched on news.google.com
		payload = {'hl': 'en', 'tbm':'	nws', 'authuser': 0, 'q': x}
		r = requests.get('https://www.google.com/search',params=payload,proxies={"http":http_proxy,"https":https_proxy})
		soup = BeautifulSoup(r.text,'html.parser')
		#foo.write(r.url+'\n'+'\n')
		#foo.write(soup.prettify().encode('utf-8').strip())
		#the classes displayed in source code when seen from chrome may not be the same when downloaded from Requests package.
		for link in soup.select("h3.r > a"):
			print(clean_(link.get('href')))
			url = clean_(link.get('href'))
			#foo.write('{"politician":"'+lastName.encode('utf-8').strip()+'", "tweet":"'+i['text'].encode('utf-8').strip()+',"url1":"'+clean_(link.get('href')).encode('utf-8').strip()+'"}\n\n')
			r2 = requests.get(url)
			soup2 = BeautifulSoup(r2.text,'html.parser')
			#print soup2.prettify() #to check if webpage is fetched or not
			foo.write(lastName.encode('utf-8').strip()+'\n\n')
			foo.write(i['text'].encode('utf-8').strip()+'\n\n')
			foo.write(clean_(link.get('href'))+'\n\n')
			for st in soup2.find_all('p'):
				foo.write(strip_tags(st.encode('utf-8').strip()))
			foo.write('\n\n\n\n'+'_____________________________________________________________________________________________________________________________________________\n\n')
			break; #for stopping after the first link only
		
