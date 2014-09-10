import requests
from datetime import datetime
from ftplib import FTP
import json
import twitter
import time
import sys

# FOR TWITTER DATA
CONSUMER_KEY = 'YOUR_CONSUMER_KEY'
CONSUMER_SECRET = 'YOUR_CUSTOMER_SECRET_KEY'
ACCESS_TOKEN_KEY = 'YOUR_ACCESS_TOKEN_KEY'
ACCESS_TOKEN_SECRET = 'YOU_ACCESS_TOKEN_SECRET_KEY'
api = twitter.Api(consumer_key = CONSUMER_KEY, consumer_secret = CONSUMER_SECRET, access_token_key = ACCESS_TOKEN_KEY, access_token_secret = ACCESS_TOKEN_SECRET)

# We need to fire a request at the coveritlive API
#COVERITLIVE API INFO
API_ENDPOINT = "https://api.coveritlive.com/remote/2/"
CIL_API_TOKEN = "YOUR COVERITLIVE TOKEN"

# For newsflashes
NEWSFLASH = "newsflash/list"
ENDPOINT = "&status=published"

#Used to keep the loop running
trigger = 1

#Questions for the user needed to start it up
ALTCAST_EVENT_CODE = raw_input('Enter the altcast code: ')
tweeters = raw_input('Enter the number of twitter users: ')

CIL_EVENT_CODE = "&event_code=" + ALTCAST_EVENT_CODE

#Formatting times
def get_time(time):
	if int(time[0:2]) > 16:
		format_time = str(int(time[0:2]) - 16) + time[2:5] + ' PM'
	elif int(time[0:2]) == 16:
		format_time = str(int(time[0:2]) - 4) + time[2:5] + ' PM'
	elif int(time[0:2]) == 0:
		format_time = str(12) + time[2:5] + ' AM'
	else:
		format_time = str(int(time[0:2]) - 4) + time[2:5] + ' AM'			
	return format_time

#Function for single twitter user
def get_user_tweets(user):
	try:
		reporter = api.GetUserTimeline(screen_name = user)
		latest_tweets = []
		for s in reporter[0:2]:
			tweet = {}
			profile = s.user
			tweet['reporter'] = profile.name
			tweet['handle'] = profile.screen_name
			tweet['status'] = s.text
			created = s.created_at
			sliced_up = created.split()
			time = sliced_up[3]
			tweet['time'] = get_time(time)
			tweet['image'] = profile.profile_image_url
						
			latest_tweets.append(tweet)
		return latest_tweets
	except:
		print 'That user does not exist. You will need to restart the program.'

#function for multiple twitter users		
def get_list_tweets(reporters):
	try:
		r_list = reporters
		load_tweets = []
		for user in r_list:
			reporter = api.GetUserTimeline(screen_name = user)
			print reporter
			for s in reporter[0:2]:
				tweet = {}
				profile = s.user
				tweet['reporter'] = profile.name
				tweet['handle'] = profile.screen_name
				tweet['status'] = s.text
				created = s.created_at
				sliced_up = created.split()
				time = sliced_up[3]
				tweet['mark_time'] = int(time.replace(':', '')) #Used to find newest tweet
				tweet['time'] = get_time(time)
				tweet['image'] = profile.profile_image_url
						
				load_tweets.append(tweet)
			
		#this whole sequence is used to find the newest tweet. 
		measure =  []
		for time in load_tweets:
			measure.append(time['mark_time'])
			
		order_list = sorted(measure, reverse=True)
		
		latest_tweets = []
		for time in order_list:
			for tweet in load_tweets:
				if time == tweet['mark_time']:
					latest_tweets.append(tweet)
							
		return latest_tweets[0:2]
	except:
		print 'One of those users does not exist. You will need to restart the program.'
		
def twitter_user_types(users):
	if int(users) == 1:
		user = raw_input('Enter the twitter handle of the user: ')
		return user
	else:
		user_list = []
		for person in xrange(int(users)):
			user_list.append(raw_input('Enter a twitter handle: '))
		return user_list
		
users = twitter_user_types(tweeters)

def main(t_users):
	#FTP credentials
	ftp = FTP('111.11.111.111') 
	ftp.login('USER', 'PASSWORD')
	ftp.cwd('PLACE/TO/STORE/JSON_FILES/')
	ftp.storlines("STOR tweets.json", open("tweets.json", 'r'))
	ftp.storlines("STOR updates.json", open("updates.json", 'r'))


	try:
		'''
		!---------------------------!
		!--- for CoverItLive API---!
		!--------------------------!
		'''		
		URL = API_ENDPOINT + NEWSFLASH + CIL_API_TOKEN + CIL_EVENT_CODE + ENDPOINT
		r = requests.get(URL)
		data = r.json()
		items = data['data']
		ticker_items = []
		for item in items:
			entry = {}
			text = item['headline']
			clean_text = text.replace('\\&#039;',"'")
			final = clean_text.replace('\&quot;',"'")
				
			pubtime = item['published_timestamp']
			time = datetime.fromtimestamp(int(pubtime)).strftime("%I:%M %p")
			if time[0] == '0':
				time = time[1:]
			
			entry['headline'] = final
			entry['published'] = time
			ticker_items.append(entry)	
			
		if type(t_users) is list:
			tweet_data = get_list_tweets(t_users)
		else:
			tweet_data = get_user_tweets(t_users)			
					
		print "Updating JSON with the following info:"
		file_tweets = 'tweets.json'
		file = open(file_tweets, 'w')
		file.write(json.dumps(tweet_data, indent = 4))
		file.close()
		print "--------------"
		print "UPDATED TWEETS - ", json.dumps(tweet_data, indent=4)
		file_updates = 'updates.json'
		file_up = open(file_updates, 'w')			
		file_up.write(json.dumps(ticker_items[0:4], indent=4))
		file_up.close()
		print "--------------"
		print "UPDATED NEWSFLASHES - ", json.dumps(ticker_items[0:4], indent=4)
			
	except:
		print "Something went wrong" 


while (trigger == 1):
	localtime = time.asctime( time.localtime(time.time()) )
	print "Firing updates, starting at ", localtime
	print "---------------"
	main(users)
	print "##########################"
	time.sleep(300)



