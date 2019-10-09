from wtforms import Form, StringField, DateField, validators, FileField, PasswordField, SubmitField, BooleanField, ValidationError
import datetime
from flask_wtf import FlaskForm
from mongohelper import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[validators.DataRequired(), validators.Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', validators=[
                             validators.DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[validators.DataRequired(), validators.EqualTo('password')])

    business = StringField('Business Name',
                           validators=[validators.DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User().find_user(username)
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User().find_email(email)
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[
                             validators.DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ExpenseForm(Form):

    item = StringField('Item', [validators.Length(
        min=3, max=35), validators.InputRequired()])
    category = StringField('Category', [validators.Length(
        min=3, max=35), validators.InputRequired()])
    cost  = StringField('Cost', [validators.regexp(
        r'^[1-9][\.\d]*(,\d+)?$'), validators.InputRequired()])
    date = DateField('Date', default=datetime.date.today)

class IncomeForm(Form):

    client = StringField('Client', [validators.Length(
        min=3, max=55), validators.InputRequired()])
    job = StringField('Job', [validators.Length(
        min=3, max=65), validators.InputRequired()])
    earnings = StringField('Earnings', [validators.regexp(
        r'^[1-9][\.\d]*(,\d+)?$'), validators.InputRequired()])
    fees = StringField('Fees (optional)', [validators.regexp(
        r'^[1-9][\.\d]*(,\d+)?$'), validators.Optional()])
    platform = StringField('Platform (optional)', [validators.Length(
        min=3, max=55), validators.Optional()])
    date = DateField('Date', default=datetime.date.today)