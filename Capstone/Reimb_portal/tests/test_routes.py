import unittest
from flask import url_for
from main import app, db
from models import Employee, Department
from forms import LoginForm
from seed_data import initialize_database

class RoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.populate_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def populate_data(self):
        initialize_database(self.app)

    def test_login_page(self):
        response = self.app.get(url_for('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.app.get(url_for('register'))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.app.post(url_for('login'), data=dict(
            email='eve.brown@nucleusteq.com',
            password='password123'
        ), follow_redirects=True)
        self.assertIn(b'Logged in successfully!', response.data)

    def test_invalid_login(self):
        response = self.app.post(url_for('login'), data=dict(
            email='user@example.com',
            password='password123'
        ), follow_redirects=True)
        self.assertIn(b'Invalid email or password!', response.data)

    def test_admin_dashboard(self):
        with self.app:
            self.app.post(url_for('login'), data=dict(
                email='john.doe@nucleusteq.com',
                password='password123'
            ), follow_redirects=True)
            response = self.app.get(url_for('admin_dashboard', admin_id=1))
            self.assertEqual(response.status_code, 200)
