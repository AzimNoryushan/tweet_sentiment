# from flask import Flask, request, render_template
# from flask_cors import CORS, cross_origin
from fastapi import FastAPI, Request
from dotenv import load_dotenv
import uvicorn
import tweepy
import os
import traceback

#import matplotlib.pyplot as plt
from datetime import date
import malaya

# app = Flask(__name__)
app = FastAPI()

# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
port = int(os.environ.get('PORT', 5000))
#model = Topic_sentiment()

@app.get("/")
# @cross_origin()
def main_page():
    return {"Alive"}

@app.post("/topic")
# @cross_origin()
async def analyze_topic(request: Request):
    body = await request.json()
    result = analyze_tweet(body['topic'])

    return result

def analyze_tweet(topic):
    positive_results = 0
    negative_results = 0
    undetected_results = 0
    
    tweets = getTweets(topic)

    if tweets == None: return "Tweets empty"

    for tweet in tweets:
        try:
            sentiment = listToString(getSentiment([tweet]))
            if(sentiment=='positive'):
                positive_results = positive_results + 1
            elif(sentiment=='negative'):
                negative_results = negative_results + 1
            else:
                undetected_results = undetected_results+1
        except Exception as e:
            traceback.print_exc

    #generate_chart(positive_results, negative_results, topic)

    return { "positive": positive_results, "negative": negative_results }

def getSentiment(message):
    try:
        model = malaya.sentiment.multinomial()
        sentiment = model.predict(message, add_neutral = False)
        message = ' '.join(message)

        return sentiment
    except:
        traceback.print_exc

# def generate_chart(positive_results, negative_results, topic):
    try:
        today = date.today()
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax.axis('equal')
        sentiment_list = ['positive', 'negative']
        data_count = [positive_results, negative_results]
        colors = ['green', "red"]
        ax.pie(data_count, labels = sentiment_list,autopct='%1.2f%%',colors=colors)
        plt.title("Sentiment of " + topic + " on Twitter on " +  today.strftime("%d/%m/%Y"))
        plt.savefig('img/{topic}_{date}.png'.format(topic=topic, date=today), dpi=300, bbox_inches='tight')
    except:
        traceback.print_exc

def getTweets(topic):
        try:
            load_dotenv()

            consumer_key = os.getenv('consumer_key')
            consumer_secret = os.getenv('consumer_secret')

            access_token = os.getenv('access_token')
            access_token_secret = os.getenv('access_token_secret')

            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)

            api = tweepy.API(auth, wait_on_rate_limit=True)

            count = 0
            max_count = 1000
            topic = topic
            geocode = '3.10559,101.6427,100km'
            tweets = []

            for tweet in tweepy.Cursor(api.search_tweets, q=topic, geocode=geocode, count=100).items():
                tweets.append(tweet.text)
                count += 1

                if count >= max_count:
                    break

            return tweets

        except:
            traceback.print_exc

def listToString(list):
    try:
        string = str(list).replace(' ', '')
        string = string.replace('[', '')
        string = string.replace(']', '')
        string = string.replace('\'', '')

        return string
    except:
        traceback.print_exc

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host='0.0.0.0')