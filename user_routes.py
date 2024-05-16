from flask import render_template, redirect, request, url_for, session
from datetime import datetime
from bson import ObjectId

import pymongo
import os

client = pymongo.MongoClient(os.environ.get("MONGODB_URI"))
db = client.get_database("total_records")
entries = db.entries

def logged_in():
    if ("email" in session):
        email = session["email"]
        user_entries = entries.find({"user_id": email})
        entries_list = list(user_entries)
        entries_list.reverse()
        return render_template("logged_in.html", user_name=email, entries=entries_list)
    else:
        return redirect(url_for("login"))

def new_entry():
    message = ''

    if ("email" in session):
        if (request.method == "POST"):
            entry_data = {
                "user_id": session["email"],
                "date": str(datetime.now()),
                "rating": request.form.get("one-number"),
                "mood": request.form.get("mood"),
                "content": request.form.get("content")
            }

            content_found = entries.find_one({"content":request.form.get("content")})

            if (content_found):
                message = 'You cannot create duplicate entries!'
                return render_template("new_entry.html", message=message)
            else:
                entries.insert_one(entry_data)
                user_entries = entries.find({"user_id": session["email"]})
                entries_list = list(user_entries)
                entries_list.reverse()
                return render_template("logged_in.html", user_name=session["email"], entries=entries_list)
        
    return render_template("new_entry.html")

def delete_entry(entry_id):
    if ("email" not in session):
        return redirect(url_for("login"))
    entries.delete_one({"_id": ObjectId(entry_id), "user_id": session["email"]})
    user_entries = entries.find({"user_id": session["email"]})

    return render_template("logged_in.html", user_name=session["email"], entries=list(user_entries))