from flask import Flask, render_template
import pymongo
import bcrypt

app = Flask(__name__, template_folder = 'templates')

client = pymongo.MongoClient("mongodb+srv://admin:ruLwEaJeXrddZVtm@cluster0.r7sglr2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.get_database("total_records")
records = db.register

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@app.route("/")
def index():
    return render_template('homepage.html')

@app.route("/login/", methods=['get', 'post'])
def login():
    return render_template('homepage.html')

if __name__ == "__main__":
    app.run(debug=True)