from flask import Flask, render_template, request, url_for, session, redirect
from webforms import SearchForm
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from search import filter_search
from flask_sqlalchemy import SQLAlchemy
import json
import os
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


## STATIC VARS
current_file_dir = os.path.dirname(__file__)
class_json_path = os.path.join(current_file_dir, "json", "classes.json")
days_map = {"M": "Monday", "T": "Tuesday", "W": "Wednesday", "Th": "Thursday", "F": "Friday"}



## DATABASE CONFIG
db_name = "database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_name
app.config["SECRET_KEY"] = "abcde"

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #create one to many relationship with courses
    classes = db.relationship("Courses")

    def __repr__(self):
        return "<Name %r>" % self.name

class Courses(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)

    #foreignkey is user id
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    class_code = db.Column(db.String(100))
    class_title = db.Column(db.String(150))
    section_number = db.Column(db.Integer)
    credit_hours = db.Column(db.Integer)
    day_of_week = db.Column(db.String(100)) 
    time = db.Column(db.String(100)) 
    professor_name = db.Column(db.String(100))



##ROUTES
@app.route('/')
def index():
    full_name = "Pushin"
    if "user" in session:
        full_name = session["user"]["userinfo"]["name"]

    return render_template('index.html', name=full_name)

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
        print(user.id)

    #store user id in session
    session["user_id"] = user.id

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

@app.route("/add_class/<class_code>/<section_num>", methods = ["POST"])
def add_class(class_code, section_num):
    if request.method == "POST":
        
        class_file = open(class_json_path)
        data = json.load(class_file)

        course_name = data[class_code]["Class Title"]
        credit_hours = data[class_code]["Credit Hours"]
        professor = data[class_code]["Professors"]
        time = data[class_code]["Sections"][int(section_num) - 1]["Times"]
        time_list = time.split(" ")
        print(time_list)


        days_in_week = {}
        for j, ele in enumerate(time_list):
            if ele[0].isupper():
                for i, char in enumerate(ele):
                    if not char.isupper():
                        continue
                    if days_map[char] not in days_in_week:
                        days_in_week[days_map[char]] = time_list[j + 1].rstrip(";")
                    else:   #if in seen, must have encountered Thursday. can't fall into else statement unless T has been added and Th is found. 
                        days_in_week[days_map["Th"]] = time_list[j + 1].rstrip(";")
                    
        for day in days_in_week:
            new_class = Courses(user_id = session["user_id"], class_code=class_code, class_title=course_name, 
            section_number = section_num, credit_hours=credit_hours, day_of_week = day, time = days_in_week[day], professor_name = professor)
            db.session.add(new_class)
            db.session.commit()
            print("class added to db.")
        
            classes = Courses.query.all()
            # classes = classes.filter(Courses.user_id)
            # rows = classes.statement.execute().fetchall()
            # for row in rows:
            #     print(row)

        return redirect("/")
    


if __name__ == '__main__':
    app.run(threaded=True, port=5000)