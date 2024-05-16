from flask import render_template, redirect, request, url_for, session
import pymongo
import os

client = pymongo.MongoClient(os.environ.get("MONGODB_URI"))
db = client.get_database("total_records")
entries = db.entries

def logged_in():
    if ("email" in session):
        email = session["email"]
        return render_template("logged_in.html", user_name=email)
    else:
        return redirect(url_for("login"))

def new_entry():
    if ("email" in session):
        email = session["email"]
        return render_template("new_entry.html", user_name=email)
    else:
        return redirect(url_for("logged_in"))

def submit_entry():
    if ("email" in session):
        entry_data = {
            "user_id":session["email"],
            "date": request.form.get("date"),
            "mood": request.form.get("mood"),
            "content": request.form.get("content")
        }

    print("Entry submitted successfully!")