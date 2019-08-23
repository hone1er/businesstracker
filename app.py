from pymongo import MongoClient, ASCENDING
import datetime
from mongohelper import Business
from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route('/')
def index():
    honecode = Business()
    return render_template('index.html', honecode=honecode, income_statement=honecode.income_statment, business_expenses=honecode.business_expenses)

@app.route('/get_expenses')
def get_expenses():
    honecode = Business()
    return render_template('expenses.html', honecode=honecode, income_statement=honecode.income_statment, business_expenses=honecode.business_expenses)



if __name__ == "__main__":
    app.run(debug=True)
    #honecode.insert_income('Argos Digital', 'Python Automation/Web Scraper', 275, ref_id=253909066, fee=27.5, platform="UpWork", date=datetime.datetime(2019,8,28))
    # honecode.insert_expenses('27" Imac', '2099.19', category='computer/electronics', date=datetime.datetime(2019, 8, 16))
    # honecode.insert_expenses('Legal Zoom', '368', category='business', date=datetime.datetime(2019, 8, 14))
    # honecode.insert_expenses('Legal Zoom RA Renewal', '159', category='business', date=datetime.datetime(2019, 8, 14))
    # honecode.insert_expenses('DevCard - Bootstrap 4 theme', '29', category='dev tools', date=datetime.datetime(2019, 8, 21))
    