import unittest

from app import create_app, db
from app.auth.models import User, Role, Permission, AnonymousUser

class TestUserModel(unittest.TestCase):
    """Test user db model."""

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client(use_cookies=True)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        #db.drop_all()
        self.app_context.pop()

    def test_hashing_password(self):
        user = User(password='testing12')
        self.assertTrue(user.password is not None)

    def test_no_password_getter(self):
        user = User(password='testing12')
        with self.assertRaises(AttributeError):
            user.password

    def test_unhashing_password(self):
        user = User(password='testing12')
        self.assertTrue(user.check_password('testing'))
        self.assertFalse(user.check_password('badpassword'))

    def test_hash_passwords_are_unique(self):
        user1_pass = User(password='testing12')
        user2_pass = User(password='testing12')
        self.assertTrue(user1_pass != user2_pass)

    def test_roles_and_permissions(self):
        Role.insert_roles()
        user = User(email="johnexample@gmail.com", password=User.set_password(User, "testing12"))
        self.assertTrue(user.can(Permission.WRITE_ARTICLE))
        self.assertTrue(user.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        user = AnonymousUser()
        self.assertFalse(user.can(Permission.COMMENT))