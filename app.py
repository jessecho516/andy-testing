from flask import Flask, render_template, request
from webforms import SearchForm
from search import make_class_list, search_class

app = Flask(__name__)

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
    return render_template('login.html')

#Pass things to index_base.html
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@app.route("/search", methods = ["POST"])
def search():
    if request.method == "POST":
        form = SearchForm()
        searched = form.searched.data
        filtered = filter_search(searched)
        print(filtered)
        return render_template("search.html", searched=searched, form = form, filtered = filtered)

def filter_search(searched):
    class_list = make_class_list("/Users/andykim_1/pushin-p3/pushin-pp/website/json/classes.json")
    results = search_class(searched, class_list)
    return results

if __name__ == '__main__':
    app.run(threaded=True, port=5000)