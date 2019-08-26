
    # TRACK EXPENSES AND INCOME WITH BUSINESS TRACKER
    # Copyright (C) 2019  Joseph Villavicencio

    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this program.  If not, see <https://www.gnu.org/licenses/>.

from pymongo import MongoClient, ASCENDING
import datetime
from mongohelper import Business, User
import os
import pandas as pd
import time
import re
from werkzeug.utils import secure_filename
from flask import Flask, render_template, redirect, send_from_directory, request, flash, url_for
from flask_bcrypt import Bcrypt
from myForms import ExpenseForm, RegistrationForm, LoginForm
from config import SECRET_KEY
from flask_login import LoginManager, login_user, current_user, logout_user, login_required


app = Flask(__name__)

UPLOAD_FOLDER = 'static/import'
ALLOWED_EXTENSIONS = {'xlsx', 'csv', 'xlrd'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = SECRET_KEY
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

conn = "mongodb://localhost:27017"
client = MongoClient(conn)
db = client.HoneCode


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



################################################### WORKING ON REGISTRATION AND LOGIN
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('income'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, business=form.business.data)
        user.add_user()
        user.get_id()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('income'))
    honecode = Business()
    form = LoginForm()
    if form.validate_on_submit():
        print(form.email.data)
        users = honecode.db.users.find({'email': form.email.data})
        for user in users:
            if user and bcrypt.check_password_hash(user['password'], form.password.data):
                user = User(username=user['username'], password=user['password'], email=user['email'], business=user['business'])
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('income'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)



######################################################################################

@app.route('/income', methods=['GET', 'POST'])
def income():
    
    # FILE UPLOAD
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            honecode = Business()
            honecode.auto_insert_income('static/import/'+filename)
            flash("UPLOADED!")
            return redirect(url_for('income'))
    # END FILE UPLOAD
    honecode = Business()
    return render_template('income.html', honecode=honecode, income_statement=honecode.income_statment, business_expenses=honecode.business_expenses)


@app.route('/get_expenses', methods=['GET', 'POST'])
def get_expenses():
    honecode = Business()
    # CREATE THE ADD EXPENSE FORM USING THE HELPER CLASS FROM myForms.py
    form = ExpenseForm(request.form)
    if request.method == 'POST' and form.validate():
        # THIS POST REQUEST ADDS AN EXPENSE TO THE DB
        try:
            honecode.insert_expenses(form)
        except:
            pass
        return redirect(url_for('get_expenses'))
    return render_template('expenses.html', form=form, honecode=honecode, income_statement=honecode.income_statment, business_expenses=honecode.business_expenses)


@app.route('/remove_expense/<expense>', methods=['POST'])
def remove_expense(expense):
    honecode = Business()
    if request.method == 'POST':
        honecode.remove_expense(expense)
    return redirect(url_for('get_expenses'))




if __name__ == "__main__":
    app.run(debug=True)