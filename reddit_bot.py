import praw
from urllib.request import urlopen
import json
import datetime
import requests

##### CONSTANTS #####
API_MENSA_IP = '836'
REDDIT_DHGE_NAME = 'dhgememes'
REDDIT_FLAIR_ID_INFORMATION = '1930f6a4-5847-11ed-bebc-7261b29a7cf9'
PRAW_CLIENT_ID = 'gCJJH0GO5aN0sjFM6zoc4w'
PRAW_CLIENT_SECRET = 'KpgXvshvdMjixot1J5grXZ3U737mHw'
PRAW_REFRESH_TOKEN = '2418566552937-xh4rG2tMISfYHeWMJl9nF29-kYGTAw'
PRAW_USER_AGENT = 'mensa-bot v1.1 by /u/MensaBot'

##### FUNCTIONS #####
def isValidUrl(url):
	return requests.head(url).status_code < 400

def jsonDataIsEmpty(data):
    return data == None

def createAndPublishRedditPost(data, date):
    global reddit

    title = f'Mittagessen vom {date.day}.{date.month}.{date.year}'
    body = 'Falls dir Verbesserungsvorschläge für diesen täglichen Post einfallen, kannst du diese gerne [💬 hier](https://github.com/MhouneyLH/dhge_mensa_bot) in Form einese Issues mitteilen.\n'

    for i in range(0, len(data)):
        meal = data[i]
        mealName = meal["name"]
        mealPriceStudents = meal["prices"]["students"]
        mealNotes = meal["notes"]

        body += f'# {mealName}\n* Preis (Studenten): {mealPriceStudents:.2f}€\n'
        for j in range(0, len(mealNotes)):
            body += f'* {mealNotes[j]}\n'
    
    reddit.subreddit(REDDIT_DHGE_NAME).submit(title, selftext = body, flair_id = REDDIT_FLAIR_ID_INFORMATION)

##### SCRIPT #####
reddit = praw.Reddit(client_id = PRAW_CLIENT_ID,
                     client_secret = PRAW_CLIENT_SECRET,
                     refresh_token = PRAW_REFRESH_TOKEN,
                     user_agent = PRAW_USER_AGENT,)

currentDate = datetime.datetime.now()
currentDateInISOFormat = currentDate.isoformat()[0:10]
API_URL = f'https://openmensa.org/api/v2/canteens/{API_MENSA_IP}/days/{currentDateInISOFormat}/meals'

if not isValidUrl(API_URL):
    exit()

apiResponse = urlopen(API_URL)
responseData = json.loads(apiResponse.read())

if jsonDataIsEmpty(responseData):
    exit()

createAndPublishRedditPost(responseData, currentDate)