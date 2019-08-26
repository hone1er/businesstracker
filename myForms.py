from wtforms import Form, StringField, DateField,validators, FileField, PasswordField, SubmitField, BooleanField
import datetime
from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[validators.DataRequired(), validators.Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[validators.DataRequired(), validators.EqualTo('password')])
                                     
    business = StringField('Business',
                            validators=[validators.DataRequired()])                                   
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ExpenseForm(Form):
 
    item = StringField('Item', [validators.Length(min=3, max=35), validators.InputRequired()])
    category = StringField('Category', [validators.Length(min=3, max=35), validators.InputRequired()])
    cost = StringField('Cost', [validators.regexp(r'^[1-9][\.\d]*(,\d+)?$'),validators.InputRequired()])
    date = DateField('Date', default=datetime.date.today)
