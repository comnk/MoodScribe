from flask import render_template, redirect, request, url_for, session
from datetime import datetime
from bson import ObjectId

import pymongo
import os

from dotenv import load_dotenv
load_dotenv()

client = pymongo.MongoClient(os.environ.get("MONGODB_URI"))
db = client.get_database("total_records")
entries = db.entries
records = db.register

def logged_in():
    if ("email" in session):
        email = session["email"]
        user_entries = entries.find({"user_id": session["email"]})
        entries_list = list(user_entries)
        entries_list.reverse()
        return render_template("logged_in.html", user_name=email, entries=entries_list)
    else:
        return redirect(url_for("login"))

def user_profile_settings():
    user = records.find_one({"email":session["email"]})

    if ("email" in session):
        if (request.method == "POST"):
            user_name = request.form.get("fullname")
            email = request.form.get("email")
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")

            user_found = records.find_one({"name":user_name})
            email_found = records.find_one({"email":email})

            if (user_found):
                message = 'There is a user already with that name!'
                return render_template("user_profile.html", user=user, message=message)
            
            if (email_found):
                message = 'This email already exists in the database!'
                return render_template("user_profile.html", user=user, message=message)
            
            if (password1 != password2 and password1 != "" and password2 != ""):
                message = 'Passwords must match!'
                return render_template("user_profile.html", user=user, message=message)
            
            else:
                user_data = {
                "name": request.form.get("fullname"),
                "email": request.form.get("email")}

                #if (password1 == ""):
                #    user_data["password"] = user_found["password"]
                #else:
                #    user_data["password"] = password1

                records.update_one({"email": session["email"]}, {"$set": user_data})

                entries.update_many(
                    {"user_id": session["email"]}, 
                    {"$set": {"user_id": request.form.get("email")}}
                )

                session["email"] = request.form.get("email")

                user_entries = entries.find({"user_id": session["email"]})
                entries_list = list(user_entries)
                entries_list.reverse()
                return render_template("logged_in.html", user_name=session["email"], entries=entries_list)
    
    return render_template("user_profile.html", user=user)