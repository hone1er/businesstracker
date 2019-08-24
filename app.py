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


# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)

@app.route('/get_expenses', methods=['GET','POST'])
def get_expenses():
    honecode = Business()
    form = ExpenseForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            honecode.insert_expenses(form.item.data, float(form.cost.data), category=form.category.data, date=datetime.datetime.combine(form.date.data, datetime.datetime.min.time()))
        except:
            honecode.insert_expenses(form.item.data, form.cost.data, category=form.category.data, date=datetime.datetime.combine(form.date.data, datetime.datetime.min.time()))
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
    #honecode.insert_income('Argos Digital', 'Python Automation/Web Scraper', 275, ref_id=253909066, fee=27.5, platform="UpWork", date=datetime.datetime(2019,8,28))
    # honecode.insert_expenses('27" Imac', '2099.19', category='computer/electronics', date=datetime.datetime(2019, 8, 16))
    # honecode.insert_expenses('Legal Zoom', '368', category='business', date=datetime.datetime(2019, 8, 14))
    # honecode.insert_expenses('Legal Zoom RA Renewal', '159', category='business', date=datetime.datetime(2019, 8, 14))
    # honecode.insert_expenses('DevCard - Bootstrap 4 theme', '29', category='dev tools', date=datetime.datetime(2019, 8, 21))
    