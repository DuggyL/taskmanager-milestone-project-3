from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html")

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(username) < 3:
            flash('username must be greater than 3 characters.', category='error')
        elif len(password1) < 6:
            flash('password must be at least 6 characters.', category='error')
        elif password1 != password2:
            flash('Password do not match.', category='error')
        else:
            new_user = User(username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('You are registered.', category='success')
            return redirect(url_for('views.home'))

        
    return render_template("register.html")

@auth.route('/logout')
def logoit():
    return "<p>Logout</p>"