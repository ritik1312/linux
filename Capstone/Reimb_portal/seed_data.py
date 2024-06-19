from werkzeug.security import generate_password_hash
from models import db, Employee, Department, Request

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
        Employee(first_name='John', last_name='Doe', email='john.doe@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='1234567890', role='ADMIN'),
        
        # Engineering Managers
        Employee(first_name='Jane', last_name='Smith', email='jane.smith@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='0987654321', department_id=1, role='MANAGER'),
        Employee(first_name='Mark', last_name='Brown', email='mark.brown@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='1231231234', department_id=1, role='MANAGER'),
        Employee(first_name='Liam', last_name='Williams', email='liam.williams@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='1234561234', department_id=1, role='MANAGER'),
        Employee(first_name='Emma', last_name='Jones', email='emma.jones@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='2345672345', department_id=1, role='MANAGER'),
        
        # Marketing Managers
        Employee(first_name='Alice', last_name='Johnson', email='alice.johnson@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='1122334455', department_id=2, role='MANAGER'),
        Employee(first_name='Olivia', last_name='Taylor', email='olivia.taylor@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='2233445567', department_id=2, role='MANAGER'),
        Employee(first_name='Sophia', last_name='Anderson', email='sophia.anderson@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='3344556678', department_id=2, role='MANAGER'),
        
        # Finance Managers
        Employee(first_name='Bob', last_name='White', email='bob.white@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='2233445566', department_id=3, role='MANAGER'),
        Employee(first_name='Mason', last_name='Martinez', email='mason.martinez@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='4455667789', department_id=3, role='MANAGER'),
        Employee(first_name='Ava', last_name='Garcia', email='ava.garcia@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='5566778890', department_id=3, role='MANAGER'),
        
        # Engineering Users
        Employee(first_name='Charlie', last_name='Black', email='charlie.black@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='3344556677', department_id=1, role='USER'),
        Employee(first_name='Dave', last_name='Green', email='dave.green@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='4455667788', department_id=1, role='USER'),
        Employee(first_name='Mia', last_name='Lee', email='mia.lee@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='5566778899', department_id=1, role='USER'),
        Employee(first_name='Noah', last_name='Clark', email='noah.clark@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='6677889901', department_id=1, role='USER'),
        Employee(first_name='Isabella', last_name='Harris', email='isabella.harris@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='7788990012', department_id=1, role='USER'),
        
        # Marketing Users
        Employee(first_name='Eve', last_name='Brown', email='eve.brown@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='5566778899', department_id=2, role='USER'),
        Employee(first_name='Frank', last_name='Yellow', email='frank.yellow@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='6677889900', department_id=2, role='USER'),
        Employee(first_name='Olivia', last_name='Young', email='olivia.young@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='8899001123', department_id=2, role='USER'),
        Employee(first_name='Lucas', last_name='King', email='lucas.king@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='9988776655', department_id=2, role='USER'),
        Employee(first_name='Ella', last_name='Wright', email='ella.wright@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='8899002234', department_id=2, role='USER'),
        
        # Finance Users
        Employee(first_name='Grace', last_name='Red', email='grace.red@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='7788990011', department_id=3, role='USER'),
        Employee(first_name='Hank', last_name='Blue', email='hank.blue@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='8899001122', department_id=3, role='USER'),
        Employee(first_name='James', last_name='Moore', email='james.moore@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='9900112233', department_id=3, role='USER'),
        Employee(first_name='Aiden', last_name='Jackson', email='aiden.jackson@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='2233445566', department_id=3, role='USER'),
        Employee(first_name='Ella', last_name='Walker', email='ella.walker@nucleusteq.com', password=generate_password_hash('Password123'), contact_no='1122334455', department_id=3, role='USER')
    ]

    try:
        for emp in employees:
            db.session.add(emp)
        
        db.session.commit()
    except Exception as e:
        return f'Error initializing Employees data'
    

def seed_requests():
    requests = [
        # Engineering Department Requests
        Request(emp_id=12, amount=12000.0, expense_type='Travelling', status='PENDING', manager_id=2, proof='12_1_download1.png', comments=None),
        Request(emp_id=12, amount=4000.0, expense_type='Tech Assets', status='PENDING', manager_id=2, proof='12_2_download3.jpeg', comments=None),
        Request(emp_id=13, amount=18000.0, expense_type='Relocation', status='APPROVED', manager_id=3, proof='13_3_download2.png', comments='Approved for Relocation expenses for new office'),
        Request(emp_id=2, amount=5000.0, expense_type='Tech Assets', status='PENDING', manager_id=1, proof='2_4_download4.jpeg', comments=None),
        Request(emp_id=2, amount=15000.0, expense_type='Travelling', status='REJECTED', manager_id=3, proof='2_5_download5.png', comments='Not valid Proof'),

        # Marketing Department Requests
        Request(emp_id=17, amount=15000.0, expense_type='Travelling', status='PENDING', manager_id=1, proof='17_6_download1.png', comments=None),
        Request(emp_id=17, amount=19000.0, expense_type='Relocation', status='APPROVED', manager_id=6, proof='17_7_download3.jpeg', comments='Approved for Moving expenses for promotion'),
        Request(emp_id=17, amount=3000.0, expense_type='Tech Assets', status='PENDING', manager_id=6, proof='17_8_download2.png', comments=None),
        Request(emp_id=6, amount=5000.0, expense_type='Tech Assets', status='REJECTED', manager_id=7, proof='6_9_download4.jpeg', comments='Request denied due to incomplete documentation'),
        Request(emp_id=7, amount=10000.0, expense_type='Travelling', status='APPROVED', manager_id=1, proof='7_10_download5.png', comments='Approved for client meeting in London'),

        # Finance Department Requests
        Request(emp_id=22, amount=14000.0, expense_type='Travelling', status='PENDING', manager_id=9, proof='22_11_download1.png', comments=None),
        Request(emp_id=22, amount=5000.0, expense_type='Tech Assets', status='APPROVED', manager_id=9, proof='22_12_download3.jpeg', comments='Approved for Purchase of accounting software'),
        Request(emp_id=23, amount=20000.0, expense_type='Relocation', status='PENDING', manager_id=1, proof='23_13_download2.png', comments=None),
        Request(emp_id=24, amount=3000.0, expense_type='Tech Assets', status='REJECTED', manager_id=1, proof='24_14_download4.jpeg', comments='Not Valid Proof'),
        Request(emp_id=9, amount=15000.0, expense_type='Travelling', status='APPROVED', manager_id=1, proof='9_15_download5.png', comments='Approved for financial summit in New York'),
    ]
    
    try:
        for req in requests:
            db.session.add(req)
        
        db.session.commit()
    except Exception as e:
        return f'Error initializing Requests data: {e}'


def initialize_database(app):
    with app.app_context():
        db.create_all()
        seed_departments()
        seed_employees()
        seed_requests()
        print("Database seeded!")
