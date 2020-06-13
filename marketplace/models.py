from datetime import datetime
from marketplace import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#db.drop_all() ... erases everything in the database
#db.create_all() ... creates the database with tables from models.py

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), unique=False, nullable=False) #not sure about this one, gotta figure out
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

#image of the car is missing - let's do it later on once it's working
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    make = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    ODO = db.Column(db.Integer(), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    fuel = db.Column(db.String(100), nullable=False)
    transmission = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"