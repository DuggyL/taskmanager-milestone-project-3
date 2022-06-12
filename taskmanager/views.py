import os
from flask import Blueprint, Flask, render_template, request
from flask_pymongo import PyMongo
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

@views.route('/')
@login_required
def home():
    tasks = mongo.db.tasks.find()
    return render_template("home.html", user=current_user)