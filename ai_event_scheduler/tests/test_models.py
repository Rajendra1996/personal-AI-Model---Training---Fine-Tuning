import unittest
from flask import current_app
from app import create_app, db
from app.models import User, Event
from werkzeug.security import generate_password_hash
from config import TestConfig

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

    def test_user_creation(self):
        u = User(username='john')
        db.session.add(u)
        db.session.commit()
        self.assertIsNotNone(User.query.filter_by(username='john').first())

    def test_user_registration(self):
        u = User(username='sally', password_hash=generate_password_hash('sallypassword'))
        db.session.add(u)
        db.session.commit()
        test_user = User.query.filter_by(username='sally').first()
        self.assertTrue(test_user.check_password('sallypassword'))
        self.assertFalse(test_user.check_password('wrongpassword'))

    def test_event_creation(self):
        u = User(username='admin')
        db.session.add(u)
        db.session.commit()
        event = Event(title="Conference", description="Tech Conference", user_id=u.id)
        db.session.add(event)
        db.session.commit()
        self.assertIsNotNone(Event.query.filter_by(title="Conference").first())

    def test_login(self):
        # Assuming you have a login function or method to test
        u = User(username='loginuser', password_hash=generate_password_hash('loginpassword'))
        db.session.add(u)
        db.session.commit()
        # Simulate login
        self.assertTrue(u.check_password('loginpassword'))
        self.assertFalse(u.check_password('wrong'))

if __name__ == '__main__':
    unittest.main()
