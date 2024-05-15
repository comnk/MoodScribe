from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template
import pymongo
import bcrypt
import os

app = Flask(__name__, template_folder = 'templates')

client = pymongo.MongoClient(os.environ.get("MONGODB_URI"))
db = client.get_database("total_records")
records = db.register

@app.route("/")
def index():
    return render_template('homepage.html')

@app.route("/login/", methods=['get', 'post'])
def login():
    return render_template('homepage.html')

if __name__ == "__main__":
    app.run(debug=True)