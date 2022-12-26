import praw
from urllib.request import urlopen
import json
import datetime

##### CONSTANTS #####
API_MENSA_IP = '836'
REDDIT_DHGE_NAME = 'dhgememes'
REDDIT_FLAIR_ID_INFORMATION = '1930f6a4-5847-11ed-bebc-7261b29a7cf9'
PRAW_CLIENT_ID = 'gCJJH0GO5aN0sjFM6zoc4w'
PRAW_CLIENT_SECRET = 'KpgXvshvdMjixot1J5grXZ3U737mHw'
PRAW_REFRESH_TOKEN = '2418566552937-xh4rG2tMISfYHeWMJl9nF29-kYGTAw'
PRAW_USER_AGENT = 'mensa-bot v1.1 by /u/MensaBot'

##### FUNCTIONS #####
def create_and_publish_reddit_post(data, date):
    global reddit

    title = f'Mittagessen vom {date.day}.{date.month}.{date.year}'
    body = 'Falls dir Verbesserungsvorschläge für diesen täglichen Post einfallen, kannst du diese gerne [💬 hier](https://github.com/MhouneyLH/dhge_mensa_bot) in Form einese Issues mitteilen.\n'

    for i in range(0, len(data)):
        meal = data[i]
        meal_name = meal["name"]
        meal_price_students = meal["prices"]["students"]
        meal_notes = meal["notes"]

        body += f'# {meal_name}\n* Preis (Studenten): {meal_price_students:.2f}€\n'
        for j in range(0, len(meal_notes)):
            body += f'* {meal_notes[j]}\n'
    
    reddit.subreddit(REDDIT_DHGE_NAME).submit(title, selftext = body, flair_id = REDDIT_FLAIR_ID_INFORMATION)

##### SCRIPT #####
reddit = praw.Reddit(client_id = PRAW_CLIENT_ID,
                     client_secret = PRAW_CLIENT_SECRET,
                     refresh_token = PRAW_REFRESH_TOKEN,
                     user_agent = PRAW_USER_AGENT,)

currentDate = datetime.datetime.now()
currentDateInISOFormat = currentDate.isoformat()[0:10]
api_url = f'https://openmensa.org/api/v2/canteens/{API_MENSA_IP}/days/{currentDateInISOFormat}/meals'

api_respose = urlopen(api_url)
response_data = json.loads(api_respose.read())

create_and_publish_reddit_post(response_data, currentDate)