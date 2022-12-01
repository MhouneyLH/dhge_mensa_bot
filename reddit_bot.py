import praw
from urllib.request import urlopen
import json
import datetime

# das hier mal anschauen, um meine Zugangsdaten verschlüsseln zu können
reddit = praw.Reddit(client_id='qJsfx6IHun-VSHRQ8H2nOA',
                     client_secret='EBTx7u5EDeG2Cq0HX9E1cpu_y2vV5w',
                     refresh_token='1064866237953-I2RCpbVRKiLi5nM36wLi0X9jVCWT3Q',
                     user_agent='cool mensa-bot v1.0 by /u/MhouneyL',)

MENSA_IP = '836'
currentDate = datetime.datetime.now()
currentDateInISOFormat = currentDate.isoformat()[0:10]

REDDIT_DHGE_NAME = 'dhgememes'
FLAIR_ID_INFORMATION = '1930f6a4-5847-11ed-bebc-7261b29a7cf9'

API_URL = f'https://openmensa.org/api/v2/canteens/{MENSA_IP}/days/{currentDateInISOFormat}/meals'
response = urlopen(API_URL)
data_json = json.loads(response.read())

title = f'Mittagessen vom {currentDate.day}.{currentDate.month}.{currentDate.year}'
body = 'Falls dir Verbesserungsvorschläge für diesen täglichen Post einfallen, kannst du diese gerne [💬 hier](https://github.com/MhouneyLH/dhge_mensa_bot) in Form einese Issues mitteilen.\n'
for i in range(0, len(data_json)):
    meal = data_json[i]
    body += f'''# {meal["name"]}
* Preis (Studenten): {meal["prices"]["students"]}€
* {meal["notes"][1]}
'''

reddit.subreddit(REDDIT_DHGE_NAME).submit(title, selftext=body, flair_id=FLAIR_ID_INFORMATION)
# rather use GitHub-CI than aws -> das hier könnte ganz interessant sein: https://docs.github.com/en/actions/examples/using-the-github-cli-on-a-runner