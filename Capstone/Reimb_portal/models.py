from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from datetime import datetime

db = SQLAlchemy()

# DB Model or schema
class Employee(UserMixin, db.Model):
    __tablename__ = 'employee'
    emp_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    contact_no = db.Column(db.String(15))
    department_id = db.Column(db.Integer, db.ForeignKey('department.dept_id'))
    role = db.Column(db.String(10), nullable=False, default='USER')

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_id(self):
        return str(self.emp_id)

class Department(db.Model):
    __tablename__ = 'department'
    dept_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

class Request(db.Model):
    __tablename__ = 'request'
    req_id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.emp_id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    expense_type = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='PENDING')
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.emp_id'), nullable=False)
    created = db.Column(db.Date, default=datetime.utcnow().date)
    proof = db.Column(db.String(120), nullable=True)
    comments = db.Column(db.Text, nullable=True)