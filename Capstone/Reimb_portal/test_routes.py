import unittest
from main import app, db
from models import Employee, Department, Request
import config
import io

class TestRoutes(unittest.TestCase):

    def setUp(self):
        app.config.from_object(config.config['testing'])
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        department = Department(name='HR')
        db.session.add(department)
        db.session.commit()

        self.department_id = department.dept_id

        admin = Employee(first_name='Admin', last_name = 'User', email='admin@nucleusteq.com', password = 'admin123', role = 'ADMIN', department_id = self.department_id)
        db.session.add(admin)
        db.session.commit()

        self.admin_id = admin.emp_id

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    # TEST CASES

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)

    def test_login_page(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)

    def register(self, first_name, last_name, email, password, contact_no, department_id, role):
        return self.app.post('/register', data=dict(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            confirm_password=password,
            contact_no=contact_no,
            department=department_id,
            role=role
        ), follow_redirects=True)

    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)
    
    def test_new_user_register(self):
        response = self.register('George', 'Brown', 'george.brown@nucleusteq.com', 'Password456', '9134509876', self.department_id, 1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful! Please login.', response.data)

        user = Employee.query.filter_by(email='george.brown@nucleusteq.com').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('Password456'))

    def test_existing_user_register(self):
        self.register('George', 'Brown', 'george.brown@nucleusteq.com', 'Password456', '9134509876', self.department_id, 1)
        response = self.register('George', 'Brown', 'george.brown@nucleusteq.com', 'Password456', '9134509876', self.department_id, 1)
        self.assertIn(b'Email id already exists!', response.data)
        self.assertEqual(response.status_code, 200)
    
    def test_new_user_register_with_invalid_company_mail(self):
        response = self.register('George', 'Brown', 'george.brown@gmail.com', 'Password456', '9134509876', self.department_id, 1)
        self.assertIn(b'Please use Company Email!', response.data)
        self.assertIn('/register', response.request.url)



    def test_existing_user_login(self):
        self.register('George', 'Brown', 'george.brown@nucleusteq.com', 'Password456', '9134509876', self.department_id, 1)
        response = self.login('george.brown@nucleusteq.com','Password456')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged in successfully!', response.data)
    
    def test_invalid_user_login(self):
        response = self.login('invalid@nucleusteq.com','Password123')
        self.assertIn(b'Invalid email or password!', response.data)
    
    def test_invalid_password_login(self):
        self.register('George', 'Brown', 'george.brown@nucleusteq.com', 'Password456', '9134509876', self.department_id, 1)
        response = self.login('george.brown@nucleusteq.com','Password123')
        self.assertIn(b'Invalid email or password!', response.data)
    
    def test_logout(self):
        self.login('admin@nucleusteq.com','admin123')
        response = self.app.get('/logout')

        # Check that the session data has been cleared
        with self.app.session_transaction() as sess:
            self.assertNotIn('admin@nucleusteq.com', sess)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/login')


# Admin functionalities Test

    def test_admin_dashboard(self):
        response = self.login('admin@nucleusteq.com','admin123')
        self.assertEqual(response.status_code, 200)
        self.assertIn('/admin_dashboard', response.request.url)

    def test_admin_add_department(self):
        self.login('admin@nucleusteq.com','admin123')
        response = self.app.post(f'/admin_dashboard/{self.admin_id}', data={
            'action': 'add_department',
            'new_department_name': 'Sales'
        })
        self.assertEqual(response.status_code, 302)
        department = Department.query.filter_by(name='Sales').first()
        self.assertIsNotNone(department)

    def test_admin_delete_department(self):
        self.login('admin@nucleusteq.com','admin123')
        self.app.post(f'/admin_dashboard/{self.admin_id}', data={
            'action': 'add_department',
            'new_department_name': 'Sales'
        })
        dept_id = Department.query.filter_by(name='Sales').first().dept_id
        response = self.app.post(f'/admin_dashboard/{self.admin_id}', data={
            'action': 'delete_department',
            'selected_department_id': dept_id
        })
        self.assertEqual(response.status_code, 302)
        department = Department.query.get(dept_id)
        self.assertIsNone(department)

    def test_admin_delete_employee(self):
        self.login('admin@nucleusteq.com','admin123')
        self.register('George', 'Brown', 'george.brown@nucleusteq.com', 'Password123', '9134509876', self.department_id, 1)
        emp_id = Employee.query.filter_by(email='george.brown@nucleusteq.com').first().emp_id

        response = self.app.post(f'/admin_dashboard/{self.admin_id}/delete_employee/{emp_id}')
        self.assertEqual(response.status_code, 302)
        employee = Employee.query.get(emp_id)
        self.assertIsNone(employee)

    def test_admin_assign_manager(self):
        self.login('admin@nucleusteq.com','admin123')

        employee = Employee(first_name='Test', last_name='Employee', email='testemployee@nucleusteq.com', password='employee123', contact_no='3156789012', department_id=self.department_id, role='MANAGER')
        db.session.add(employee)
        db.session.commit()

        manager = Employee(first_name='Test', last_name='Manager', email='testmanager@nucleusteq.com', password='manager123', contact_no='3456789012', department_id=employee.department_id, role='MANAGER')
        db.session.add(manager)
        db.session.commit()

        claim = Request(
            emp_id=employee.emp_id, 
            amount=4000, 
            expense_type='Travelling',
            manager_id=self.admin_id
            )
        db.session.add(claim)
        db.session.commit()
        req_id = claim.req_id

        response = self.app.post(f'/admin_dashboard/{self.admin_id}/assign_manager/{req_id}', data={
            'manager': manager.emp_id
        })
        self.assertEqual(response.status_code, 302)
        
        claim = Request.query.get(req_id)
        self.assertEqual(claim.manager_id, manager.emp_id)

    def test_admin_approve_claim(self):
        self.login('admin@nucleusteq.com','admin123')

        employee = Employee(first_name='Test', last_name='Employee', email='testemployee@nucleusteq.com', password='employee123', contact_no='3156789012', department_id=self.department_id, role='MANAGER')
        db.session.add(employee)
        db.session.commit()

        claim = Request(
            emp_id=employee.emp_id, 
            amount=4000, 
            expense_type='Travelling',
            manager_id=self.admin_id
            )
        db.session.add(claim)
        db.session.commit()
        req_id = claim.req_id

        response = self.app.post(f'/admin_dashboard/{self.admin_id}/approve_reject_claim/{req_id}', data={
            'action': 'approve_claim',
            'comments': 'Approved'
        })
        self.assertEqual(response.status_code, 302)
        
        claim = Request.query.get(req_id)
        self.assertEqual(claim.status, 'APPROVED')
        self.assertEqual(claim.comments, 'Approved')

    def test_admin_reject_claim(self):
        self.login('admin@nucleusteq.com','admin123')

        employee = Employee(first_name='Test', last_name='Employee', email='testemployee@nucleusteq.com', password='employee123', contact_no='3156789012', department_id=self.department_id, role='MANAGER')
        db.session.add(employee)
        db.session.commit()

        claim = Request(
            emp_id=employee.emp_id, 
            amount=4000, 
            expense_type='Travelling',
            manager_id=self.admin_id
            )
        db.session.add(claim)
        db.session.commit()
        req_id = claim.req_id

        response = self.app.post(f'/admin_dashboard/{self.admin_id}/approve_reject_claim/{req_id}', data={
            'action': 'reject_claim',
            'comments': 'No valid proofs'
        })
        self.assertEqual(response.status_code, 302)
        
        claim = Request.query.get(req_id)
        self.assertEqual(claim.status, 'REJECTED')
        self.assertEqual(claim.comments, 'No valid proofs')

# Manager Functionalities Check

    def submit_reimbursement(self, emp_id, email, amount, expense_type):
        data=dict(
            email = email,
            amount = amount,
            expense_type = expense_type
        )
        return self.app.post(f'/dashboard/{emp_id}/submitreimbursement', data=data, content_type='multipart/form-data', follow_redirects=True)

    def test_manager_dashboard(self):
        self.register('Manager', 'User', 'manager@nucleusteq.com', 'manager123', '9134509876', self.department_id, 2)
        response = self.login('manager@nucleusteq.com', 'manager123')
        self.assertEqual(response.status_code, 200)
        self.assertIn('/manager_dashboard', response.request.url)

    def test_mmanager_approve_claim(self):
        self.register('Manager', 'User', 'manager@nucleusteq.com', 'manager123', '9134509876', self.department_id, 2)
        self.login('manager@nucleusteq.com', 'manager123')
        manager_id = Employee.query.filter_by(email='manager@nucleusteq.com').first().emp_id

        employee = Employee(first_name='Test', last_name='Employee', email='testemployee@nucleusteq.com', password='employee123', contact_no='3156789012', department_id=self.department_id, role='MANAGER')
        db.session.add(employee)
        db.session.commit()

        claim = Request(
            emp_id=employee.emp_id, 
            amount=4000, 
            expense_type='Travelling',
            manager_id=manager_id
            )
        db.session.add(claim)
        db.session.commit()
        req_id = claim.req_id

        response = self.app.post(f'/manager_dashboard/{manager_id}/approve_reject_claim/{req_id}', data={
            'action': 'approve_claim',
            'comments': 'Approved'
        })
        self.assertEqual(response.status_code, 302)
        
        claim = Request.query.get(req_id)
        self.assertEqual(claim.status, 'APPROVED')
        self.assertEqual(claim.comments, 'Approved')



    def test_mmanager_reject_claim(self):
        self.register('Manager', 'User', 'manager@nucleusteq.com', 'manager123', '9134509876', self.department_id, 2)
        self.login('manager@nucleusteq.com', 'manager123')
        manager_id = Employee.query.filter_by(email='manager@nucleusteq.com').first().emp_id

        employee = Employee(first_name='Test', last_name='Employee', email='testemployee@nucleusteq.com', password='employee123', contact_no='3156789012', department_id=self.department_id, role='MANAGER')
        db.session.add(employee)
        db.session.commit()

        claim = Request(
            emp_id=employee.emp_id, 
            amount=4000, 
            expense_type='Travelling',
            manager_id=manager_id
            )
        db.session.add(claim)
        db.session.commit()
        req_id = claim.req_id

        response = self.app.post(f'/manager_dashboard/{manager_id}/approve_reject_claim/{req_id}', data={
            'action': 'reject_claim',
            'comments': 'Not Valid Proofs'
        })
        self.assertEqual(response.status_code, 302)
        
        claim = Request.query.get(req_id)
        self.assertEqual(claim.status, 'REJECTED')
        self.assertEqual(claim.comments, 'Not Valid Proofs')
    
    def test_manager_submit_request(self):
        self.register('Manager', 'User', 'manager@nucleusteq.com', 'manager123', '9134509876', self.department_id, 2)
        self.login('manager@nucleusteq.com', 'manager123')
        manager = Employee.query.filter_by(email='manager@nucleusteq.com').first()
        response = self.submit_reimbursement(manager.emp_id, manager.email, 4000, 'Travelling')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reimbursement request submitted successfully!', response.data)

        request = Request.query.filter_by(emp_id=manager.emp_id).first()
        self.assertIsNotNone(request)
        self.assertEqual(request.amount, 4000)
        self.assertEqual(request.expense_type, 'Travelling')


# Employee Functionalities Check

    def test_employee_dashboard(self):
        self.register('Employee', 'User', 'employee@nucleusteq.com', 'employee123', '9134509874', self.department_id, 1)
        response = self.login('employee@nucleusteq.com', 'employee123')
        self.assertEqual(response.status_code, 200)
        self.assertIn('/employee_dashboard', response.request.url)
    
    def test_employee_submit_request_invalid_email(self):
        self.register('Employee', 'User', 'employee@nucleusteq.com', 'employee123', '9134509874', self.department_id, 1)
        self.login('employee@nucleusteq.com', 'employee123')
        employee = Employee.query.filter_by(email='employee@nucleusteq.com').first()
        response = self.submit_reimbursement(employee.emp_id, 'invalid@nucleusteq.com', 4000, 'Travelling')
        self.assertIn(b'Invalid email! Please enter your email.', response.data)
    
    def test_employee_submit_request_valid_email(self):
        self.register('Employee', 'User', 'employee@nucleusteq.com', 'employee123', '9134509874', self.department_id, 1)
        self.login('employee@nucleusteq.com', 'employee123')
        employee = Employee.query.filter_by(email='employee@nucleusteq.com').first()
        response = self.submit_reimbursement(employee.emp_id, employee.email, 4000, 'Travelling')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reimbursement request submitted successfully!', response.data)

        request = Request.query.filter_by(emp_id=employee.emp_id).first()
        self.assertIsNotNone(request)
        self.assertEqual(request.amount, 4000)
        self.assertEqual(request.expense_type, 'Travelling')

if __name__ == '__main__':
    unittest.main()
