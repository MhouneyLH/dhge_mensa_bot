import datetime
import json
import praw
import random
import requests
from urllib.request import urlopen

##### CONSTANTS #####
API_MENSA_IP = '836'
REDDIT_DHGE_NAME = 'dhgememes'
REDDIT_FLAIR_ID_INFORMATION = '1930f6a4-5847-11ed-bebc-7261b29a7cf9'
PRAW_CLIENT_ID = 'gCJJH0GO5aN0sjFM6zoc4w'
PRAW_CLIENT_SECRET = 'KpgXvshvdMjixot1J5grXZ3U737mHw'
PRAW_REFRESH_TOKEN = '2418566552937-xh4rG2tMISfYHeWMJl9nF29-kYGTAw'
PRAW_USER_AGENT = 'mensa-bot v1.1 by /u/MensaBot'
POST_BODY_INFORMATION_MESSAGE = 'Falls dir Verbesserungsvorschlรคge fรผr diesen tรคglichen Post oder generell fรผr diesen Bot einfallen, kannst du diese gerne [๐ฌ hier](https://github.com/MhouneyLH/dhge_mensa_bot) in Form einese Issues mitteilen.\n'
FOOD_EMOJIS = [ '๐', '๐', '๐', '๐ญ', '๐ฟ', '๐ฅ', '๐ณ', '๐ฅ', '๐ฅ', '๐ฅช', '๐ฎ', '๐ฏ', '๐', '๐',
                '๐ฅฉ', '๐ฅ', '๐ฅ ', '๐ฅก', '๐ค', '๐ฃ', '๐ฆช', '๐', '๐', '๐', '๐', '๐', '๐ง', '๐ฅ',
                '๐ฒ', '๐', '๐ฅฃ', '๐ฐ', '๐', '๐ช', '๐ฅฆ', '๐ถ', '๐ต', '๐ฅฎ', '๐ฅ', '๐ง', '๐ฅ', '๐ฅฏ',
                '๐ฅจ', '๐ฅ', '๐', ] 

##### FUNCTIONS #####
def isValidUrl(url):
	return requests.head(url).status_code < 400

def jsonDataIsEmpty(data):
    return data == None

def checkDayAndMonth(date, day, month):
    return  date.day == day and date.month == month

def getRandomFoodEmoji():
    randomNumber = random.randint(0, len(FOOD_EMOJIS) - 1)
    return FOOD_EMOJIS[randomNumber]

def createAndPublishRedditPost(data, date):
    global reddit

    title = f'Mittagessen vom {date.day}.{date.month}.{date.year}'
    body = POST_BODY_INFORMATION_MESSAGE

    for i in range(0, len(data)):
        meal = data[i]
        mealName = meal["name"]
        mealPriceStudents = meal["prices"]["students"]
        mealNotes = meal["notes"]

        body += f'# {mealName} {getRandomFoodEmoji()}\n* Preis (Studenten): {mealPriceStudents:.2f}โฌ\n'
        for j in range(0, len(mealNotes)):
            body += f'* {mealNotes[j]}\n'
    
    reddit.subreddit(REDDIT_DHGE_NAME).submit(title, selftext = body, flair_id = REDDIT_FLAIR_ID_INFORMATION)

def createAndPublishSpecialRedditPosts(date):
    global reddit

    title = ''
    body = POST_BODY_INFORMATION_MESSAGE

    if checkDayAndMonth(date, 14, 2):
        title = 'Einen schรถnen Valentinstag, wรผnscht euch der DHGE-Reddit-Bot! ๐๐น'
    elif checkDayAndMonth(date, 8, 3):
        title = 'Einen tollen Frauentag, wรผnscht euch der DHGE-Reddit-Bot! ๐ฉ๐ป๐๐ป'
    elif checkDayAndMonth(date, 9, 4): # @todo: Ostern muss angepasst werden
        title = 'Frohe Ostern, wรผnscht euch der DHGE-Reddit-Bot! Viel Spaร beim Suchen. ๐ฐ๐'
    elif checkDayAndMonth(date, 1, 5):
        title = 'Einen wunderschรถnen Tag der Arbeit, wรผnscht euch der DHGE-Reddit-Bot! In diesem Sinne: Coded, was das Zeug hรคlt! ๐จ๐ป'
    elif checkDayAndMonth(date, 14, 5): # @todo: Muttertag muss angepasst werden
        title = 'Der DHGE-Reddit-Bot wรผnscht allen Mรผttern einen wundervollen Muttertag! ๐คฐ๐ป'
    elif checkDayAndMonth(date, 18, 5): # @todo: Mรคnnertag muss angepasst werden
        title = 'Einen erfolgreichen Mรคnnertag, wรผnscht euch der DHGE-Reddit-Bot! ๐คต๐ป๐ป'
    elif checkDayAndMonth(date, 28, 5): # @todo: Pfingsten muss angepasst werden
        title = 'Ein ruhiges und entspannendes Pfingstfest, wรผnscht euch der DHGE-Reddit-Bot! ๐คต๐ป๐ป'
    elif checkDayAndMonth(date, 20, 9):
        title = 'Zumindest fรผr alle, die in Thรผringen wohnen, wรผnscht euch der DHGE-Reddit-Bot einen frohen Weltkindertag! ๐ง๐ง๐ป๐ง๐ผ๐ง๐ฝ๐ง๐พ๐ง๐ฟ'
    elif checkDayAndMonth(date, 3, 10):
        title = 'Einen geschichtstrรคchtigen Tag der deutschen Einheit, wรผnscht euch der DHGE-Reddit-Bot! ๐ฉ๐ช'
    elif checkDayAndMonth(date, 31, 10):
        title = 'Happy Halloween, wรผnscht euch der DHGE-Reddit-Bot! ๐๐น'
    elif checkDayAndMonth(date, 6, 12):
        title = 'Einen schรถnen Nikolaustag, wรผnscht euch der DHGE-Reddit-Bot! ๐๐ป'
    elif checkDayAndMonth(date, 24, 12):
        title = 'Frohe Weihnachten und ein besinnliches Fest, wรผnscht euch der DHGE-Reddit-Bot! ๐๐๐ป๐'
    elif checkDayAndMonth(date, 25, 12):
        title = 'Einen frohen und besinnlichen 1. Weihnachtsfeiertag, wรผnscht euch der DHGE-Reddit-Bot! ๐๐๐'
    elif checkDayAndMonth(date, 26, 12):
        title = 'Einen frohen und besinnlichen 2. Weihnachtsfeiertag, wรผnscht euch der DHGE-Reddit-Bot! ๐๐๐'
    elif checkDayAndMonth(date, 31, 12):
        title = 'Frohes neues Jahr, wรผnscht euch der DHGE-Reddit-Bot! ๐งจ๐ Ich hoffe, dass ihr alles schafft, was ihr euch fรผr dieses Jahr vorgenommen habt. ๐'
    else:
        return

    reddit.subreddit(REDDIT_DHGE_NAME).submit(title, selftext = body, flair_id = REDDIT_FLAIR_ID_INFORMATION)


##### SCRIPT #####
reddit = praw.Reddit(client_id = PRAW_CLIENT_ID,
                     client_secret = PRAW_CLIENT_SECRET,
                     refresh_token = PRAW_REFRESH_TOKEN,
                     user_agent = PRAW_USER_AGENT,)

currentDate = datetime.datetime.now()
currentDateInISOFormat = currentDate.isoformat()[0:10]

API_URL = f'https://openmensa.org/api/v2/canteens/{API_MENSA_IP}/days/{currentDateInISOFormat}/meals'

# this has to be executed before the url-check
# on holiday the url-check exits the script
createAndPublishSpecialRedditPosts(currentDate)

if not isValidUrl(API_URL):
    exit()

apiResponse = urlopen(API_URL)
responseData = json.loads(apiResponse.read())
if jsonDataIsEmpty(responseData):
    exit()

createAndPublishRedditPost(responseData, currentDate)