# Author: Akshit Arora
# Date Generated: June 21 2016, 1:42pm
# Script aims to collect 200 tweets of given politicians' twitter handles. And then save it all in JSON format in a single output.txt file.

#twitter handles of politicians we are interested in:
#Donald Trump - "realDonaldTrump"
#Hillary Clinton - "HillaryClinton"
#Narendra Modi - "narendramodi"
#Barack Obama - "POTUS" or "BarackObama" POTUS =president of the united states		#Arvind Kejriwal - "ArvindKejriwal"

import tweepy
import json
import os

#API access keys (obtained from http://dev.twitter.com )
consumer_key = "dDxZfIhGQmfhRL4Jvpy1MwmSH"
consumer_secret = "rALldhXAliKzLfeMKwRd0BDATbpGh7BOuNDbdud9E2egNbYIBX"
access_token = "1555165788-gzBceCbuo00zemOCv8aeqSPguAGXExtXwhvkZ2D"
access_token_secret = "ifukcgo8Xnt0Li0pcBzXK5V47KqNaWuDSfmFlTckMvaNG"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth_handler=auth,proxy="https://anz148198:07h5AK79bL@10.10.78.61:3128")
#public_tweets = api.home_timeline() #testing twitter API working
#wb+ helps open file in write binary and it creates file if it does not already exists
fo = open("output.txt","wb+")
#defining a dictionary of politicianName:twitterHandles
#politicians = {'trump':'realDonaldTrump', 'clinton':'HillaryClinton', 'modi':'narendramodi'}
politicians = {'cynthia_mckinney':'cynthiamckinney', 'hillary_clinton':'HillaryClinton', 'gary_johnson':'GovGaryJohnson', 'donald_trump':'realDonaldTrump', 'barack_obama':'BarackObama'}
fo.write('{')
for lastName, twitterHandle in politicians.iteritems():
	fo.write('\n'+'"'+lastName+'": [')
	politicianid = api.get_user(twitterHandle)
	politicianid2 = politicianid.id
	donald = api.user_timeline(politicianid2,count=200)
	for tweet in donald:
		print tweet.text
		print '\n' #for displaying line separated tweets, just as a check
		json_str = json.dumps(tweet._json)
		fo.write('\n'+'\n'+json_str+',')
	fo.close()
	with open("output.txt", 'rb+') as filehandle:
	    filehandle.seek(-1, os.SEEK_END)
	    filehandle.truncate()
	fo = open("output.txt","a")
	fo.write('],')
fo.close()
with open("output.txt", 'rb+') as filehandle:
	filehandle.seek(-1, os.SEEK_END)
	filehandle.truncate()
fo = open("output.txt","a")
fo.write('}')
