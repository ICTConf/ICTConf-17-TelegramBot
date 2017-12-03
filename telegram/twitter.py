
import tweepy
from twitter_config import *

class Twitter:
	def __init__(self):

		self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		self.auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
		self.api = tweepy.API(self.auth)
		
	def send_media_tweet(self,image,content):
	
		self.api.update_with_media(filename=image,status=content)
		
	def send_tweet(self,content):
		
		self.api.update_status(status=content)
			
