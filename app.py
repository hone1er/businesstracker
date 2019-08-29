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
import os
import pandas as pd
import time
import re
from werkzeug.utils import secure_filename
from flask import Flask, render_template, redirect, send_from_directory, request, flash, url_for
from flask_bcrypt import Bcrypt
from config import SECRET_KEY, mongop
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin
from myForms import ExpenseForm, RegistrationForm, LoginForm, IncomeForm
from mongohelper import Business, User


app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname('__file__'),'static/import')
ALLOWED_EXTENSIONS = {'xlsx', 'csv', 'xlrd'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = SECRET_KEY
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

conn = f'mongodb+srv://hone1er:{mongop}@incometracker-blo7g.azure.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(conn)
db = client.HoneCode
users = db.users



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



 
########### LOGIN/REGISTRATION/LOGOUT ##################

@login_manager.user_loader
def load_user(username):
    u = db.users.find_one({"username": username})
    if not u:
        return None
    return User(username=u['username'], business=u['business'], email=u['email'])


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('income'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_password, business=form.business.data)
        user.add_user()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('income'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.users.find_one({'email': form.email.data})
        if user and bcrypt.check_password_hash(user['password'], form.password.data):
            user = User(username=user['username'],
                        business=user['business'], email=user['email'])
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('income'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

######################################################################################


@app.route('/', methods=['GET', 'POST'])
@login_required
def income():
    # FILE UPLOAD
    form = IncomeForm(request.form)
    if request.method == 'POST':
        if len(request.form) == 0:
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
                honecode = Business(current_user.username)
                honecode.auto_insert_income('static/import/'+filename)
                flash("UPLOADED!")
                return redirect(url_for('income'))
        else:
            Business(current_user.username).add_income(form)
    # END FILE UPLOAD
    honecode = Business(current_user.username)
    return render_template('income.html', form=form, honecode=honecode, income_statement=honecode.income_list, business_expenses=honecode.expense_list)


@app.route('/get_expenses', methods=['GET', 'POST'])
@login_required
def get_expenses():
    honecode = Business(current_user.username)
    # CREATE THE ADD EXPENSE FORM USING THE HELPER CLASS FROM myForms.py
    form = ExpenseForm(request.form)
    if request.method == 'POST' and form.validate():
        # THIS POST REQUEST ADDS AN EXPENSE TO THE DB WHEN 'ADD' IS CLICKED ON THE get_expenses PAGE
        try:
            honecode.insert_expenses(form)
        except:
            pass
        return redirect(url_for('get_expenses'))
    return render_template('expenses.html', form=form, honecode=honecode, income_statement=honecode.income_list, business_expenses=honecode.expense_list)


@app.route('/remove_expense/<expense>', methods=['POST'])
@login_required
def remove_expense(expense):
    ''' removes an expense based on the item_id '''
    if request.method == 'POST' :
        Business(current_user.username).remove_expense(expense, users)
    return redirect(url_for('get_expenses'))



@app.route('/remove_income/<income>', methods=['POST'])
@login_required
def remove_income(income):
    ''' removes an incomebased on the item_id '''
    if request.method == 'POST':
        print(income)
        Business(current_user.username).remove_income(income)
    return redirect(url_for('income'))



@app.route('/add_income', methods=['POST'])
@login_required
def add_income():
    ''' adds an incomebased on the item_id '''
    form = IncomeForm(request.form)
    if request.method == 'POST' and form.validate():
        Business(current_user.username).add_income(form)
    return redirect(url_for('income'))


if __name__ == "__main__":
    app.run(debug=True)
