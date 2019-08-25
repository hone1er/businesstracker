import datetime
import re
import pandas as pd
from pymongo import MongoClient
from bson.objectid import ObjectId


class Business:
    def __init__(self):
        # CONNECT TO MONGODB
        conn = "mongodb://localhost:27017"
        client = MongoClient(conn)
        self.db = client.HoneCode
        self.business_expenses_collection = self.db.business_expenses
        self.income_collection = self.db.income
        self.income_statment = self.income_collection.find()
        self.business_expenses = self.business_expenses_collection.find()
        
        self.expenses = self.business_expenses_collection.aggregate([
            {
                '$group':
                {
                    '_id': {},
                    'totalAmount': {'$sum': "$item.cost"},
                    'count': {'$sum': 1}
                }
            }
        ])

        self.income = self.income_collection.aggregate([
            {
                '$group':
                {
                    '_id': {},
                    'totalAmount': {'$sum': "$income.total"},
                    'count': {'$sum': 1}
                }
            }
        ])

        self.total_fees = self.income_collection.aggregate([
            {
                '$group':
                {
                    '_id': {},
                    'totalAmount': {'$sum': "$income.fee.amount"},
                    'count': {'$sum': 1}
                }
            }
        ])

    def insert_income(self, name, job, amount, ref_id=None, fee=None, fee_ref=None, platform=None, date=None):
        ''' manually insert data '''
        if name == None or job == None:
            return
        if date == None:
            date = datetime.datetime.utcnow()
        self.income_collection.insert_one({'client': {'name': name, 'job': {'name': job, 'date': date, 'platform': platform, 'ref_id': ref_id}}, 'income': {
                                          'total': float(amount), 'fee': {'amount': fee, 'ref_id': fee_ref}, 'net': (float(amount)-float(fee))}})

    def auto_insert_income(self, csv):
        ''' for csv files downloaded from UpWork '''

        df = pd.read_csv(csv)
        df = df[['Date', 'Ref ID', 'Type', 'Team', 'Amount', 'Description']]
        months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                  'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
        iterable = iter(df.iterrows())
        for idx, row in iterable:
            if idx < len(df)-1:
                typehead = row[2]
                nexttype = df.iloc[idx+1]['Type']
                month = months[''.join(re.findall('[a-zA-Z]', row[0]))]

                day, year = int(row[0][4::].split(',')[0]), int(
                    row[0][4::].split(',')[1])

                if typehead == 'Service Fee' and nexttype == 'Hourly':
                    date = datetime.datetime(year, month, day)
                    fee_id = str(row[1])
                    job_id = str(df.iloc[idx+1]['Ref ID'])
                    client = row[3]
                    fee_amount = float(row[4])
                    income = float(df.iloc[idx+1]['Amount'])
                    job_description = df.iloc[idx+1]['Description']
                    net = float(income) - float(fee_amount)
                    self.db.income.insert_one({'client': {'name': client, 'job': {'name': job_description, 'date': date, 'platform': 'UpWork', 'ref_id': job_id}}, 'income': {
                                              'total': income, 'fee': {'amount': fee_amount, 'ref_id': fee_id}, 'net': net}})

    def insert_expenses(self, item_name, cost, receiptIMG=None, category=None, date=None):
        self.business_expenses_collection.insert_one(
            {'item': {'name': item_name, 'category': category, 'cost': cost, 'receipt': receiptIMG}, 'date': date})

    def remove_expense(self, id):
        found = {"_id": ObjectId(id)}
        result = self.db.business_expenses.delete_one(found)
        print(result.deleted_count)
