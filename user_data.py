from flask import render_template, redirect, request, url_for, session
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import pymongo
import json
import os

from dotenv import load_dotenv
load_dotenv()

client = pymongo.MongoClient(os.environ.get("MONGODB_URI"))
db = client.get_database("total_records")
entries = db.entries

def user_sentiment_scores():
    if ("email" in session):
        analyzer = SentimentIntensityAnalyzer()

        email = session["email"]
        user_entries = entries.find({"user_id": email})
        entries_list = list(user_entries)
        display_data = []

        for entry in entries_list:
            sentence = "Today, {} feels like a {}/10, his emotion word is '{}' and he said this: '{}'".format(email, entry["rating"], entry["mood"], entry["content"])
            vs = analyzer.polarity_scores(sentence)
            display_data.append({"date":entry["date"].split(" ")[0], "sentiment":vs["compound"]})
        
        print(display_data)
    
    return render_template("analyze_data.html", data=display_data)