#twitter handles of politicians we are interested in:
#Donald Trump - "realDonaldTrump"
#Hillary Clinton - "HillaryClinton"
#Barack Obama - "POTUS" or "BarackObama" POTUS =president of the united states
#Arvind Kejriwal - "ArvindKejriwal"
#Narendra Modi - "narendramodi"

#for later comparison
# Cynthia McKinney - "cynthiamckinney"
# Gary Johnson - "GovGaryJohnson"
# George Bush - "GeorgeHWBush"
# John Edwards - "LouisianaGov"
# Mitt Romney - "MittRomney"
# Ralph Nader - "RalphNader"
consumer_key = "dDxZfIhGQmfhRL4Jvpy1MwmSH"
consumer_secret = "rALldhXAliKzLfeMKwRd0BDATbpGh7BOuNDbdud9E2egNbYIBX"
access_token = "1555165788-gzBceCbuo00zemOCv8aeqSPguAGXExtXwhvkZ2D"
access_token_secret = "ifukcgo8Xnt0Li0pcBzXK5V47KqNaWuDSfmFlTckMvaNG"
import tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth_handler=auth,proxy="https://akshita.visitor:nuwZHYHt@10.10.78.21:3128")
public_tweets = api.home_timeline()
trump = api.get_user('HillaryClinton')
trump2 = trump.id
donald = api.user_timeline(trump2,count=100)
fo = open("test_clinton.txt","wb")
for tweet in donald:
	print tweet.text
	print '\n'
	fo.write((tweet.text.encode('utf-8').strip())+'\n') #only in python2.7 is such concatenation of bytes type and string type possible (not in python3)

fo.close()
