import datetime
from pymongo import MongoClient

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
        self.total_fees = self.income_collection.aggregate( [
     {
       '$group':
         {
            '_id': {},
           'totalAmount': { '$sum': "$income.fee.amount" },
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

