from flask import Flask, render_template, request, url_for, session, redirect
from webforms import SearchForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from search import filter_search
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import find_dotenv, load_dotenv
from authlib.integrations.flask_client import OAuth
from os import environ as env
from urllib.parse import quote_plus, urlencode


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

db_name = "database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_name
app.config["SECRET_KEY"] = "abcde"

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    classes = db.relationship("Courses")

    def __repr__(self):
        return "<Name %r>" % self.name

class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_code = db.Column(db.String(100), unique=True)
    class_title = db.Column(db.String(150), unique=True)
    credit_hours = db.Column(db.Integer)
    times = db.Column(db.String(100)) 
    professor_name = db.Column(db.String(100))


@app.route('/')
def index():
    return render_template('index.html')

import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    # if "user" in session:
    #     print(session["user"])
    token = oauth.auth0.authorize_access_token()
    session["user"] = token

    email = session["user"]["userinfo"]["email"]
    full_name = session["user"]["userinfo"]["name"]

    user = Users.query.filter_by(email=email).first()
    if not user:
        user = Users(name=full_name, email=email)
        db.session.add(user)
        db.session.commit()
        print("user added to db.")
    else:
        print("user found in db.")

    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

#Pass things to index_base.html
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@app.route("/search", methods = ["POST"])
def search():
    class_list = []
    if request.method == "POST":
        form = SearchForm()
        searched = form.searched.data
        
    if len(searched) == 0:
        return render_template('index.html')

    filtered = filter_search(searched)
    return render_template("search.html", searched=searched, form = form, filtered = filtered)

@app.route("/add_class", methods = ["POST"])
def add_class():
    # if request.method == "POST":
    #     if request.form["add_class"]:
    print("add button pressed.")
        
        # return render_template("index.html")
    



if __name__ == '__main__':
    app.run(threaded=True, port=5000)