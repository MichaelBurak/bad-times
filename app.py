import time
import schedule
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import requests
import os
from dotenv import load_dotenv
from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
import time

# create flask app
app = Flask(__name__)

load_dotenv()

KEY = os.getenv('KEY')

titles = []


def job():
    global titles
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

    titles = ",".join([article['title'] for article in five_worst])
    print(titles)


# create schedule for printing time
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=job,
    trigger=IntervalTrigger(seconds=30),
    id='printing_time_job',
    name='Print time every 2 seconds',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

# def home(stories=stories):
#     return render_template('index.html', stories=stories)


@app.route('/')
def home():
    return render_template('index.html', titles=titles)


# run Flask app in debug mode
app.run(debug=True)
