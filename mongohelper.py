import datetime
import re
import pandas as pd
from pymongo import MongoClient
from bson.objectid import ObjectId
import time
from flask_login import UserMixin


class Business:
    def __init__(self, username):
        # CONNECT TO MONGODB
        conn = "mongodb+srv://hone1er:Penalbaby1@incometracker-blo7g.azure.mongodb.net/test?retryWrites=true&w=majority"
        client = MongoClient(conn)
        self.db = client.HoneCode
        self.username = username
        # attempt to retrieve data from MongoDB, if none available, set income_list and expense_list to empty list []
        try:
            self.expense_list = []
            for i in self.db.users.find({'username': username}):
                for j in i['expenses']:
                    self.expense_list.append(j)
        except:
            self.expense_list = []
        try:
            self.income_list = []
            for i in self.db.users.find({'username': username}):
                for j in i['clients']:
                    self.income_list.append(j)
        except:
            self.income_list = []

        # Try calculating expenses, fees, and total. If no figures available, set to 0
        try:
            expenses = self.db.users.find({'username': username})
            fees = self.db.users.find({'username': username})
            total = self.db.users.find({'username': username})
            for expense in expenses:
                self.total_expenses = sum([i['cost']
                                           for i in expense['expenses']])

            for fee in fees:
                self.total_fees = sum(
                    [i['income']['fee']['amount'] for i in fee['clients']])

            for amount in total:
                self.total_income = sum([i['income']['total']
                                         for i in amount['clients']])

        except:
            self.total_expenses = 0
            self.total_fees = 0
            self.total_income = 0

    def insert_income(self, name, job, amount, ref_id=None, fee=None, fee_ref=None, platform=None, date=None):
        ''' manually insert data '''
        if name == None or job == None:
            return
        if date == None:
            date = datetime.datetime.utcnow()
        self.db.users.insert_one({'username': self.username, 'client': {'name': name, 'job': {'name': job, 'date': date, 'platform': platform, 'ref_id': ref_id}}, 'income': {
            'total': float(amount), 'fee': {'amount': fee, 'ref_id': fee_ref}, 'net': (float(amount)+float(fee))}})

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
                    if self.db.users.count_documents({'clients.job.ref_id': job_id}) == 0:
                        client = row[3]
                        fee_amount = float(row[4])
                        income = float(df.iloc[idx+1]['Amount'])
                        job_description = df.iloc[idx+1]['Description']
                        net = float(income) + float(fee_amount)
                        self.db.users.update(
                            {'username': self.username}, {'$push': {'clients': {'name': client, 'job': {'name': job_description, 'date': date, 'platform': 'UpWork', 'ref_id': job_id}, 'income': {
                                'total': income, 'fee': {'amount': fee_amount, 'ref_id': fee_id}, 'net': net}}}}, upsert=True)

    def insert_expenses(self, form, receiptIMG=None):
        self.db.users.update(
            {'username': self.username}, {'$push': {'expenses': {'item_id': ObjectId(), 'name': form.item.data, 'category': form.category.data, 'cost': float(form.cost.data)*-(1), 'receipt': receiptIMG, 'date': datetime.datetime.combine(form.date.data, datetime.datetime.min.time())}}}, upsert=True)

    def remove_expense(self, eid):
        self.db.users.update(
            {},
            {'$pull': {'expenses': {'item_id': ObjectId(eid)}}}
        )

    def remove_income(self, iid):
        self.db.users.update(
            {},
            {'$pull': {'clients': {'job.ref_id': iid}}}
        )


class User(UserMixin):
    def __init__(self, username=None, email=None, password=None, business=None):
        # CONNECT TO MONGODB
        conn = "mongodb+srv://hone1er:Penalbaby1@incometracker-blo7g.azure.mongodb.net/test?retryWrites=true&w=majority"
        client = MongoClient(conn)
        self.db = client.HoneCode
        self.username = username
        self.business = business
        self.password = password
        self.email = email

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def add_user(self):
        self.db.users.insert_one(
            {'username': self.username, 'password': self.password, 'email': self.email, 'business': self.business})

    def find_email(self, email):
        if self.db.users.count_documents({'email': email.data}) > 0:
            return 1
        return None

    def find_user(self, user):
        if self.db.users.count_documents({'username': user.data}) > 0:
            return 1
        return None

    def get_user(self):
        return self.username

    def get_name(self):
        return self.username

    def get_id(self):
        return self.username
