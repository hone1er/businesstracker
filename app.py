from pymongo import MongoClient, ASCENDING
import datetime
from flask import Flask, render_template, redirect

app = Flask(__name__)



class Business:
    def __init__(self):
        # CONNECT TO MONGODB
        conn = "mongodb://localhost:27017"
        client = MongoClient(conn)
        db = client.HoneCode
        self.business_expenses_collection = db.business_expenses
        self.income_collection = db.income
        self.income_statment = self.income_collection.find()
        self.business_expenses = self.business_expenses_collection.find()

        self.expenses = self.business_expenses_collection.aggregate( [
     {
       '$group':
         {
            '_id': {},
           'totalAmount': { '$sum': "$item.cost" },
           'count': { '$sum': 1 }
         }
     }
   ])

        self.income = self.income_collection.aggregate( [
     {
       '$group':
         {
            '_id': {},
           'totalAmount': { '$sum': "$income.total" },
           'count': { '$sum': 1 }
         }
     }
   ])
        


    def insert_income(self, name, job, amount, ref_id=None, fee=None, fee_ref=None, platform=None, date=None):
        ''' manually insert data '''
        if name == None or job == None:
            return
        if date == None:
            date = datetime.datetime.utcnow()
        self.income_collection.insert_one({'client': {'name': name, 'job': {'name': job, 'date': date, 'platform': platform, 'ref_id': ref_id}}, 'income': {'total': float(amount), 'fee': {'amount': fee, 'ref_id': fee_ref}, 'net': (float(amount)-float(fee))}})


    def auto_insert_income(self, csv):
        ''' for csv files downloaded from UpWork '''
        # date =
        # dtype = 
        # description = 
        # client_name =
        # amount =
        # ref_id = 
        pass

    def insert_expenses(self, item_name, cost, receiptIMG=None, category=None, date=None):
        self.business_expenses_collection.insert_one({'item': {'name': item_name, 'category': category, 'cost': cost, 'receipt': receiptIMG}, 'date': date})

    def get_income(self):
        print("JOBS")
        for job in self.income_statment:
            income = float(job['income']['total'])
            print(f"CLIENT: {job['client']['name']} INCOME: {income} DATE: {job['client']['job']['date']}")
            self.income += income
            

    def get_expenses(self):
        print("EXPENSES")
        for expense in self.business_expenses:
            cost = float(expense['item']['cost'])
            print(f"ITEM: {expense['item']['name']}\nCOST: {cost}\nDATE: {expense['date']}\n\n\n")
            self.expenses += cost
    
    def estimate_tax(self, percent=.3):
        self.taxes = self.income * percent


@app.route('/')
def index():
    honecode = Business()
    return render_template('index.html', honecode=honecode, income_statement=honecode.income_statment, expenses=honecode.business_expenses)


if __name__ == "__main__":
    app.run(debug=True)
    print(honecode.expenses)
    print(honecode.income)
    print( honecode.income - honecode.expenses)
    #honecode.insert_income('Argos Digital', 'Python Automation/Web Scraper', 275, ref_id=253909066, fee=27.5, platform="UpWork", date=datetime.datetime(2019,8,28))
    # honecode.insert_expenses('27" Imac', '2099.19', category='computer/electronics', date=datetime.datetime(2019, 8, 16))
    # honecode.insert_expenses('Legal Zoom', '368', category='business', date=datetime.datetime(2019, 8, 14))
    # honecode.insert_expenses('Legal Zoom RA Renewal', '159', category='business', date=datetime.datetime(2019, 8, 14))
    # honecode.insert_expenses('DevCard - Bootstrap 4 theme', '29', category='dev tools', date=datetime.datetime(2019, 8, 21))
    