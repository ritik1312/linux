from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, URLField, FloatField, FileField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange
from flask_wtf.file import FileAllowed
import re
import email_validator

def valid_company_domain(form, field):
    allowed_domain = "nucleusteq.com"
    email = field.data
    if not email.endswith(f"@{allowed_domain}"):
        raise ValidationError('Please use Company Email!')

def check_password_requirement(form, field):
    password = field.data
    if not re.search(r'[A-Z]', password) or not re.search(r'[0-9]', password):
        raise ValidationError('Password must contain atleast 1 digit and 1 uppercase!')
    

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    signup_link = URLField('Not registered Yet', default='/register')


class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), valid_company_domain])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Password must be atleast 8 characters long!'), check_password_requirement])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords don\'t match!')])
    contact_no = StringField('Contact Number', validators=[DataRequired(), Length(min=10, max=10, message='Enter a valid 10-digit contact number!')])
    department = SelectField('Department', choices=[('','Select Department')], default='')
    role = SelectField('Select Role', choices=[(1,'User'),(2,'Manager')], default=1)
    submit = SubmitField('Register')
    login_link = URLField('Already Registered', default='/login')


class ReimbursementForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    expense_type = SelectField('Expense Type', choices=[('Travelling', 'Travelling'), ('Relocation', 'Relocation'), ('Tech_assets', 'Tech Assets')], validators=[DataRequired()])
    receipt = FileField('Receipt', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'pdf'], 'Images and PDFs only!')])
