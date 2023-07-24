from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
import pyrebase
from datetime import datetime

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyA5rGXu34Ktpn1ysQ0OrSmcYIgbCOI8PPY",
  "authDomain": "y2labs.firebaseapp.com",
  "projectId": "y2labs",
  "storageBucket": "y2labs.appspot.com",
  "messagingSenderId": "126408756000",
  "appId": "1:126408756000:web:078006a5c57fc42c37e545",
  "measurementId": "G-08PW8WZZR7",
  "databaseURL": "https://y2labs-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        try:
            email = request.form["email"]
            password = request.form["password"]
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:

            pass
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            email = request.form["email"]
            password = request.form["password"]
            login_session['user'] = auth.create_user_with_email_and_password(email, password)

            inputs = {
                "fullname": request.form["fullname"], "bio": request.form["bio"],
                "username": request.form["username"], "email": email,
            }
            db.child("Users").child(login_session["user"]["localId"]).set(inputs)

            return redirect(url_for('add_tweet'))
        except:
            pass
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == "POST":
        try:
            db.child("Tweets").push({
                "title": request.form["title"],
                "text": request.form["text"],
                "uid": login_session["user"]["localId"],
                "timestamp": datetime.now(),
                "likes": 0
            })
        except:
            pass

    return render_template("add_tweet.html")

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/all_tweets')
def all_tweets():
    return render_template('all_tweets.html', tweets=db.child('Tweets').get().val())

@app.route("/like/<tweet>", methods=['GET', 'POST'])
def like(tweet):
    if request.method == "POST":
        tweet_s = db.child("Tweets").child(tweet)
        tweet_s.update({"likes": tweet_s.get().val()["likes"] + 1})
    return redirect(url_for('all_tweets'))

if __name__ == '__main__':
    app.run(debug=True)
