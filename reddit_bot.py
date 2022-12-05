import praw
from urllib.request import urlopen
import json
import datetime

##### CONSTANTS #####
MENSA_IP = '836'
REDDIT_DHGE_NAME = 'dhgememes'
FLAIR_ID_INFORMATION = '1930f6a4-5847-11ed-bebc-7261b29a7cf9'

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

        body += f'# {meal_name}\n* Preis (Studenten): {meal_price_students}€\n'
        for j in range(0, len(meal_notes)):
            body += f'* {meal_notes[j]}\n'
    
    reddit.subreddit(REDDIT_DHGE_NAME).submit(title, selftext=body, flair_id=FLAIR_ID_INFORMATION)

##### SCRIPT #####
reddit = praw.Reddit(client_id='qJsfx6IHun-VSHRQ8H2nOA',
                     client_secret='EBTx7u5EDeG2Cq0HX9E1cpu_y2vV5w',
                     refresh_token='1064866237953-I2RCpbVRKiLi5nM36wLi0X9jVCWT3Q',
                     user_agent='cool mensa-bot v1.0 by /u/MhouneyL',)

currentDate = datetime.datetime.now()
currentDateInISOFormat = currentDate.isoformat()[0:10]
api_url = f'https://openmensa.org/api/v2/canteens/{MENSA_IP}/days/{currentDateInISOFormat}/meals'

api_respose = urlopen(api_url)
response_data = json.loads(api_respose.read())

create_and_publish_reddit_post(response_data, currentDate)