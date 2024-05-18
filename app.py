from flask import Flask, render_template, request, url_for, redirect, session
from dotenv import load_dotenv

import bcrypt
import os
import pymongo
import user_routes
import edit_entry

load_dotenv()

app = Flask(__name__, template_folder = 'templates')
app.secret_key = "testing"

app.add_url_rule('/logged_in/', view_func=user_routes.logged_in)
app.add_url_rule('/new_entry/', view_func=edit_entry.new_entry, methods=['get', 'post'])
app.add_url_rule('/edit_profile/', view_func=user_routes.user_profile_settings, methods=['get', 'post'])
app.add_url_rule('/edit_entry/<entry_id>', view_func=edit_entry.edit_entry, methods=['get', 'post', 'delete'])
app.add_url_rule('/delete_entry/<entry_id>', view_func=edit_entry.delete_entry, methods=['get', 'post', 'delete'])

client = pymongo.MongoClient(os.environ.get("MONGODB_URI"))
db = client.get_database("total_records")
entries = db.entries
records = db.register

@app.route("/")
def index():
    if ("email" in session):
        user_entries = entries.find({"user_id": session["email"]})
        entries_list = list(user_entries)
        entries_list.reverse()
        return render_template("logged_in.html", user_name=session["email"], entries=entries_list)

    return render_template('landing_page.html')

@app.route("/registration/", methods=['get', 'post'])
def registration():
    message = ''

    if ("email" in session):
        user_entries = entries.find({"user_id": session["email"]})
        entries_list = list(user_entries)
        entries_list.reverse()
        return render_template("logged_in.html", user_name=session["email"], entries=entries_list)
    
    if (request.method == "POST"):
        user = request.form.get("fullname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user_found = records.find_one({"name":user})
        email_found = records.find_one({"email":email})

        if (user_found):
            message = 'There is a user already with that name!'
            return render_template("registration.html", message=message)
        
        if (email_found):
            message = 'This email already exists in the database!'
            return render_template("registration.html", message=message)
        
        if (password1 != password2):
            message = 'Passwords must match!'
            return render_template("registration.html", message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode("utf-8"), bcrypt.gensalt())
            user_info = {"name":user, "email":email, "password":hashed}
            records.insert_one(user_info)

            user_name = records.find_one({"name":user})
            new_user = user_name["name"]

            return render_template("logged_in.html", user_name=new_user)

    return render_template('registration.html')

@app.route("/login/", methods=['get', 'post'])
def login():
    message = 'Please log into account'

    if ("email" in session):
        user_entries = entries.find({"user_id": session["email"]})
        entries_list = list(user_entries)
        entries_list.reverse()
        return render_template("logged_in.html", user_name=session["email"], entries=entries_list)
    
    if (request.method == "POST"):
        email = request.form.get("email")
        password = request.form.get("password")
        email_found = records.find_one({"email":email})

        if (email_found):
            email_val = email_found["email"]
            password_check = email_found["password"]

            if (bcrypt.checkpw(password.encode('utf-8'), password_check)):
                session['email'] = email_val
                return redirect(url_for("logged_in", user_name=email_val))
            else:
                if (email in session):
                    return redirect(url_for("logged_in"))
                message = "Wrong password"
                return render_template("login.html", message=message)
        else:
            message="Email not found"
            return render_template('login.html', message=message)

    return render_template('login.html', message=message)

@app.route("/logged_out/")
def logged_out():
    if ("email" in session):
        session.pop("email", None)
        return render_template("logged_out.html")
    else:
        return render_template("landing_page.html")

if __name__ == "__main__":
    app.run(debug=True)