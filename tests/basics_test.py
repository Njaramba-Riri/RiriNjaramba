import unittest

from flask import current_app
from app import create_app, db

class TestBasicsCase(unittest.TestCase):
    """Test if the basics of the application are working as expected."""

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client(use_cookies=True)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])