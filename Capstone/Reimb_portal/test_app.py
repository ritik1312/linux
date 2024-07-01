import unittest
from flask import current_app
from main import app
import config

class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config.from_object(config.config['testing'])
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])


if __name__ == '__main__':
    unittest.main()