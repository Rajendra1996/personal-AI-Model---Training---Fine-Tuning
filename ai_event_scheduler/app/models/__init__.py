from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.Text)
    email = db.Column(db.String(120), unique=True, nullable=True)
    last_login = db.Column(db.DateTime)
    login_count = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    user = db.relationship('User', backref=db.backref('events', lazy="dynamic"))
    date = db.Column(db.DateTime)
    ticket_price = db.Column(db.Float)
    total_revenue = db.Column(db.Float)
    attendee_count = db.Column(db.Integer, default=0)
    average_rating = db.Column(db.Float)
    event_type = db.Column(db.String(64))  # New field for event type

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), index=True)
    event = db.relationship('Event', backref=db.backref('feedbacks', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('feedbacks', lazy=True))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime)


class Resource(db.Model):
    __tablename__ = 'resource'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), index=True)
    event = db.relationship('Event', backref=db.backref('resources', lazy=True))
    name = db.Column(db.String(128))
    quantity = db.Column(db.Integer)
    cost = db.Column(db.Float)
