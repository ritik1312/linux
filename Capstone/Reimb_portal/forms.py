from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, URLField, FloatField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange
from flask_wtf.file import FileAllowed
import email_validator

def company_email(form, field):
    allowed_domain = "nucleusteq.com"
    if not field.data.endswith(f"@{allowed_domain}"):
        flash('Please enter Company Email!')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    signup_link = URLField('Not registered Yet', default='/register')


class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), company_email])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    contact_no = StringField('Contact Number', validators=[DataRequired(), Length(min=10, max=15)])
    department = SelectField('Department', choices=[('','Select Department')], default='')
    role = SelectField('Select Role', choices=[(1,'User'),(2,'Manager')], default=1)
    submit = SubmitField('Register')
    login_link = URLField('Already Registered', default='/login')


class ReimbursementForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    expense_type = SelectField('Expense Type', choices=[('Travelling', 'Travelling'), ('Relocation', 'Relocation'), ('Tech_assets', 'Tech Assets')], validators=[DataRequired()])
    receipt = FileField('Receipt', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'pdf'], 'Images and PDFs only!')])
