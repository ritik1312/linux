import unittest
from main import app, db
from models import Employee, Department, Request

class ModelsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_department_creation(self):
        dept = Department(name='Human Resource')
        db.session.add(dept)
        db.session.commit()
        self.assertEqual(dept.name, 'Human Resource')

    def test_employee_creation(self):
        dept = Department(name='Human Resource')
        db.session.add(dept)
        db.session.commit()
        emp = Employee(first_name='Test', last_name='User1', email='testuser1@nucleusteq.com', password='password123', role='USER', contact_no='2134567890', departmennt_id=dept.dept_id)
        db.session.add(emp)
        db.session.commit()
        self.assertEqual(emp.email, 'testuser@nucleusteq.com')

    def test_request_creation(self):
        emp = Employee(first_name='Test', last_name='User2', email='testuser2@nucleusteq.com', password='password', role='USER')
        manager = Employee(first_name='Test', last_name='Manager2', email='testmanager2@nucleusteq.com', password='password', role='MANAGER')
        db.session.add(emp)
        db.session.commit()
        req = Request(emp_id=emp.emp_id, amount=1000, expense_type='Travelling', manager_id=manager.emp_id)
        db.session.add(req)
        db.session.commit()
        self.assertEqual(req.amount, 1000)
