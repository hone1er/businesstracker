
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
from mongohelper import Business
import os
import pandas as pd
import time
import re
from werkzeug.utils import secure_filename
from flask import Flask, render_template, redirect, send_from_directory, request, flash, url_for
from myForms import ExpenseForm
from config import SECRET_KEY


app = Flask(__name__)

UPLOAD_FOLDER = 'static/import'
ALLOWED_EXTENSIONS = {'xlsx', 'csv', 'xlrd'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = SECRET_KEY


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    honecode = Business()
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
            return redirect(url_for('index'))
    return render_template('index.html', honecode=honecode, income_statement=honecode.income_statment, business_expenses=honecode.business_expenses)


@app.route('/get_expenses', methods=['GET', 'POST'])
def get_expenses():
    honecode = Business()
    form = ExpenseForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            honecode.insert_expenses(form.item.data, float(form.cost.data)*-(1), category=form.category.data,
                                     date=datetime.datetime.combine(form.date.data, datetime.datetime.min.time()))
        except:
            honecode.insert_expenses(form.item.data, form.cost.data, category=form.category.data,
                                     date=datetime.datetime.combine(form.date.data, datetime.datetime.min.time()))
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
