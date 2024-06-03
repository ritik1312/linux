# seed_data.py

from flask import Flask
from werkzeug.security import generate_password_hash
from models import db, Employee, Department, Request  # Adjust the import as per your project structure

def seed_departments():
    departments = [
        Department(name='Engineering'),
        Department(name='Marketing'),
        Department(name='Finance')
    ]
    try:
        for dept in departments:
            db.session.add(dept)
        
        db.session.commit()
    except Exception as e:
        return f'Error initializing Departments data'

def seed_employees():
    employees = [
        # Admin
        Employee(first_name='John', last_name='Doe', email='john.doe@nucleusteq.com', password=generate_password_hash('password123'), contact_no='1234567890', role='ADMIN'),
        
        # Engineering Managers
        Employee(first_name='Jane', last_name='Smith', email='jane.smith@nucleusteq.com', password=generate_password_hash('password123'), contact_no='0987654321', department_id=1, role='MANAGER'),
        Employee(first_name='Mark', last_name='Brown', email='mark.brown@nucleusteq.com', password=generate_password_hash('password123'), contact_no='1231231234', department_id=1, role='MANAGER'),
        
        # Marketing Managers
        Employee(first_name='Alice', last_name='Johnson', email='alice.johnson@nucleusteq.com', password=generate_password_hash('password123'), contact_no='1122334455', department_id=2, role='MANAGER'),
        
        # Finance Managers
        Employee(first_name='Bob', last_name='White', email='bob.white@nucleusteq.com', password=generate_password_hash('password123'), contact_no='2233445566', department_id=3, role='MANAGER'),
        
        # Engineering Users
        Employee(first_name='Charlie', last_name='Black', email='charlie.black@nucleusteq.com', password=generate_password_hash('password123'), contact_no='3344556677', department_id=1, role='USER'),
        Employee(first_name='Dave', last_name='Green', email='dave.green@nucleusteq.com', password=generate_password_hash('password123'), contact_no='4455667788', department_id=1, role='USER'),
        
        # Marketing Users
        Employee(first_name='Eve', last_name='Brown', email='eve.brown@nucleusteq.com', password=generate_password_hash('password123'), contact_no='5566778899', department_id=2, role='USER'),
        Employee(first_name='Frank', last_name='Yellow', email='frank.yellow@nucleusteq.com', password=generate_password_hash('password123'), contact_no='6677889900', department_id=2, role='USER'),
        
        # Finance Users
        Employee(first_name='Grace', last_name='Red', email='grace.red@nucleusteq.com', password=generate_password_hash('password123'), contact_no='7788990011', department_id=3, role='USER'),
        Employee(first_name='Hank', last_name='Blue', email='hank.blue@nucleusteq.com', password=generate_password_hash('password123'), contact_no='8899001122', department_id=3, role='USER')
    ]

    try:
        for emp in employees:
            db.session.add(emp)
        
        db.session.commit()
    except Exception as e:
        return f'Error initializing Employees data'


def initialize_database(app):
    with app.app_context():
        db.create_all()
        seed_departments()
        seed_employees()
        print("Database seeded!")
