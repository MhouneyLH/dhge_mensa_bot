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
POST_BODY_INFORMATION_MESSAGE = 'Falls dir Verbesserungsvorschläge für diesen täglichen Post oder generell für diesen Bot einfallen, kannst du diese gerne [💬 hier](https://github.com/MhouneyLH/dhge_mensa_bot) in Form einese Issues mitteilen.\n'
FOOD_EMOJIS = [ '🍕', '🍔', '🍟', '🌭', '🍿', '🥓', '🍳', '🥗', '🥙', '🥪', '🌮', '🌯', '🍖', '🍗',
                '🥩', '🥟', '🥠', '🥡', '🍤', '🍣', '🦪', '🍜', '🍛', '🍚', '🍙', '🍘', '🧆', '🥘',
                '🍲', '🍝', '🥣', '🍰', '🎂', '🍪', '🥦', '🌶', '🍵', '🥮', '🍥', '🧀', '🥖', '🥯',
                '🥨', '🥐', '🍞', ] 

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

        body += f'# {mealName} {getRandomFoodEmoji()}\n* Preis (Studenten): {mealPriceStudents:.2f}€\n'
        for j in range(0, len(mealNotes)):
            body += f'* {mealNotes[j]}\n'
    
    reddit.subreddit(REDDIT_DHGE_NAME).submit(title, selftext = body, flair_id = REDDIT_FLAIR_ID_INFORMATION)

def createAndPublishSpecialRedditPosts(date):
    global reddit

    title = ''
    body = POST_BODY_INFORMATION_MESSAGE

    if checkDayAndMonth(date, 14, 2):
        title = 'Einen schönen Valentinstag, wünscht euch der DHGE-Reddit-Bot! 💘🌹'
    elif checkDayAndMonth(date, 8, 3):
        title = 'Einen tollen Frauentag, wünscht euch der DHGE-Reddit-Bot! 👩🏻💃🏻'
    elif checkDayAndMonth(date, 9, 4): # @todo: Ostern muss angepasst werden
        title = 'Frohe Ostern, wünscht euch der DHGE-Reddit-Bot! Viel Spaß beim Suchen. 🐰🐇'
    elif checkDayAndMonth(date, 1, 5):
        title = 'Einen wunderschönen Tag der Arbeit, wünscht euch der DHGE-Reddit-Bot! In diesem Sinne: Coded, was das Zeug hält! 🔨💻'
    elif checkDayAndMonth(date, 14, 5): # @todo: Muttertag muss angepasst werden
        title = 'Der DHGE-Reddit-Bot wünscht allen Müttern einen wundervollen Muttertag! 🤰🏻'
    elif checkDayAndMonth(date, 18, 5): # @todo: Männertag muss angepasst werden
        title = 'Einen erfolgreichen Männertag, wünscht euch der DHGE-Reddit-Bot! 🤵🏻🍻'
    elif checkDayAndMonth(date, 28, 5): # @todo: Pfingsten muss angepasst werden
        title = 'Ein ruhiges und entspannendes Pfingstfest, wünscht euch der DHGE-Reddit-Bot! 🤵🏻🍻'
    elif checkDayAndMonth(date, 20, 9):
        title = 'Zumindest für alle, die in Thüringen wohnen, wünscht euch der DHGE-Reddit-Bot einen frohen Weltkindertag! 🧒🧒🏻🧒🏼🧒🏽🧒🏾🧒🏿'
    elif checkDayAndMonth(date, 3, 10):
        title = 'Einen geschichtsträchtigen Tag der deutschen Einheit, wünscht euch der DHGE-Reddit-Bot! 🇩🇪'
    elif checkDayAndMonth(date, 31, 10):
        title = 'Happy Halloween, wünscht euch der DHGE-Reddit-Bot! 🎃👹'
    elif checkDayAndMonth(date, 6, 12):
        title = 'Einen schönen Nikolaustag, wünscht euch der DHGE-Reddit-Bot! 🎅🏻'
    elif checkDayAndMonth(date, 24, 12):
        title = 'Frohe Weihnachten und ein besinnliches Fest, wünscht euch der DHGE-Reddit-Bot! 🎁🎅🏻🎁'
    elif checkDayAndMonth(date, 25, 12):
        title = 'Einen frohen und besinnlichen 1. Weihnachtsfeiertag, wünscht euch der DHGE-Reddit-Bot! 🎄🎁🎄'
    elif checkDayAndMonth(date, 26, 12):
        title = 'Einen frohen und besinnlichen 2. Weihnachtsfeiertag, wünscht euch der DHGE-Reddit-Bot! 🎇🎄🎇'
    elif checkDayAndMonth(date, 31, 12):
        title = 'Frohes neues Jahr, wünscht euch der DHGE-Reddit-Bot! 🧨🎆 Ich hoffe, dass ihr alles schafft, was ihr euch für dieses Jahr vorgenommen habt. 🚀'
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