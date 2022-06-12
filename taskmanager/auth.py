import os
from flask import Blueprint, Flask, render_template, request, flash, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

def get_tasks():
    tasks = mongo.db.tasks.find()
    return render_template("tasks.html", tasks=tasks)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST": 
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect username or password, try again.', category='error')
        else:
            flash('Username or password does not exist', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1') 
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username or password already exist', category='error')
        elif password1 != password2:
            flash('Password do not match.', category='error')
        else:
            new_user = User(username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('You are registered.', category='success')
            return redirect(url_for('views.home'))

        
    return render_template("register.html", user=current_user)

@auth.route('/logout')
@login_required
def logoit():
    logout_user()
    return redirect(url_for('auth.login'))