from wtforms import Form, StringField, DateField, validators, FileField, PasswordField, SubmitField, BooleanField, ValidationError, SelectField, widgets
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
                        validators=[validators.DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[
                             validators.DataRequired()], render_kw={"placeholder": "Password"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ExpenseForm(Form):

    item = StringField('Item', [validators.Length(
        min=3, max=35), validators.InputRequired()], render_kw={"placeholder": "Item"})
    category = SelectField('Category', [validators.InputRequired()], choices=[("Business","Business"), ("Computer Hardware", "Computer Hardware"), ("Computer Software", "Computer Software"), ("Web Hosting", "Web Hosting"), ("Office Supplies", "Office Supplies")])
    cost  = StringField('Cost', [validators.regexp(
        r'^[1-9][\.\d]*(,\d+)?$'), validators.InputRequired()], render_kw={"placeholder": "Cost"})
    # receipt = FileField('Upload Receipt')
    date = DateField('Date', default=datetime.date.today)

class IncomeForm(Form):

    client = StringField('Client', [validators.Length(
        min=3, max=55), validators.InputRequired()], render_kw={"placeholder": "Client"})
    job = StringField('Job', [validators.Length(
        min=3, max=65), validators.InputRequired()], render_kw={"placeholder": "Job"})
    earnings = StringField('Earnings', [validators.regexp(
        r'^[1-9][\.\d]*(,\d+)?$'), validators.InputRequired()], render_kw={"placeholder": "Earnings"})
    fees = StringField('Fees (optional)', [validators.regexp(
        r'^[1-9][\.\d]*(,\d+)?$'), validators.Optional()], render_kw={"placeholder": "Fees"})
    platform = StringField('Platform (optional)', [validators.Length(
        min=3, max=55), validators.Optional()], render_kw={"placeholder": "Platform"})
    date = DateField('Date', default=datetime.date.today)