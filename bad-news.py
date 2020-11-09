import time
import schedule
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import requests
import os
from dotenv import load_dotenv
load_dotenv()

KEY = os.getenv('KEY')


def job():
    url = ('http://newsapi.org/v2/top-headlines?'
           'country=us&'
           f'apiKey={KEY}')
    response = requests.get(url)
    json = response.json()

    titles = []
    for i in json['articles']:
        pol = TextBlob(i['title']).sentiment.polarity
        titles.append({"title": i['title'], "pol": pol})

    five_worst = sorted((i for i in titles), key=lambda k: k['pol'])[0:6]

    for t in five_worst:
        print(t['title'])


schedule.every().hour.do(job)
# schedule.every(20).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
