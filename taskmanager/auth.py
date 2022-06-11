from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

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
    return render_template("login.html")

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1') 
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()

        if user:
            flash('Username or password already exist', category='error')
        elif len(username) < 3:
            flash('username must be greater than 3 characters.', category='error')
        elif len(password1) < 6:
            flash('password must be at least 6 characters.', category='error')
        elif password1 != password2:
            flash('Password do not match.', category='error')
        else:
            new_user = User(username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('You are registered.', category='success')
            return redirect(url_for('views.home'))

        
    return render_template("register.html")

@auth.route('/logout')
@login_required
def logoit():
    logout_user()
    return redirect(url_for('auth.login'))