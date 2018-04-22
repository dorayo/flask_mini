from app import create_app, db
from app.models import User
import unittest
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='张三')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='张三', email='zhangsan@example.com')
        self.assertEqual(u.avatar(128), 'https://www.gravatar.com/avatar/\
                         f0c3acd8a5e2b954b76bfd774a667cf1?d=identicon&s=128')


if __name__ == '__main__':
    unittest.main(verbosity=2)

