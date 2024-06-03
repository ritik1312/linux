import unittest
from flask import current_app
from main import app

class BasicTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])
