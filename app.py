from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
import pyrebase

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
  "databaseURL": ""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route('/signin', methods=['GET', 'POST'])
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
            return redirect(url_for('add_tweet'))
        except:
            pass
    return render_template("signup.html")


@app.route('/', methods=['GET', 'POST'])
def add_tweet():
    if login_session['user'] == None:
        return redirect(url_for('signin'))
    return render_template("add_tweet.html")

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)
