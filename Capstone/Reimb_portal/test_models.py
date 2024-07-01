import unittest
from main import app, db
from models import Employee, Department, Request

class TestModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app_context = app.app_context()
        cls.app_context.push()
        db.drop_all()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_department_creation(self):
        dept = Department(
            name='Human Resource'
            )
        try:
            db.session.add(dept)
            db.session.commit()
        except Exception as e:
            print(f'Error creating new department: {e}')
        self.assertIsNotNone(dept.dept_id)

    def test_employee_creation(self):
        dept_id = Department.query.filter_by(name='Human Resource').first().dept_id
        emp = Employee(
            first_name='Test', 
            last_name='User1', 
            email='testuser1@nucleusteq.com', 
            password='Password123', 
            contact_no='2134567890', 
            department_id=dept_id, 
            role='USER'
            )
        try:
            db.session.add(emp)
            db.session.commit()
        except Exception as e:
            print(f'Error creating new employee: {e}')
        self.assertIsNotNone(emp.emp_id)

    def test_request_creation(self):
        employee = Employee.query.filter_by(email='testuser1@nucleusteq.com').first()
        manager = Employee(first_name='Test', last_name='Manager2', email='testmanager2@nucleusteq.com', password='Password123', contact_no='3456789012', department_id=employee.department_id, role='MANAGER')
        try:
            db.session.add(manager)
            db.session.commit()
        except Exception as e:
            print(f'Error while adding new Manager: {e}')

        req = Request(
            emp_id=employee.emp_id, 
            amount=2000, 
            expense_type='Travelling', 
            manager_id=manager.emp_id
            )
        try:
            db.session.add(req)
            db.session.commit()
        except Exception as e:
            print(f'Error while creating new Request: {e}')
        self.assertIsNotNone(req.req_id)

if __name__ == '__main__':
    unittest.main()