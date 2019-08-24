from wtforms import Form, StringField, DateField,validators, FileField
import datetime
class ExpenseForm(Form):
 
    item = StringField('Item', [validators.Length(min=3, max=35), validators.InputRequired()])
    category = StringField('Category', [validators.Length(min=3, max=35), validators.InputRequired()])
    cost = StringField('Cost', [validators.regexp(r'^[1-9][\.\d]*(,\d+)?$'),validators.InputRequired()])
    date = DateField('Date', default=datetime.date.today)
