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
    orders = db.relationship('Order', backref='author', lazy=True)
    reviews = db.relationship('Review', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    condition = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    ODO = db.Column(db.Integer(), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    fuel = db.Column(db.String(100), nullable=False)
    transmission = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    description = db.Column(db.Text, nullable=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    orders = db.relationship('Order', backref='item', lazy=True)
    reviews = db.relationship('Review', backref='item', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer(), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=True)
    address1 = db.Column(db.String(100), nullable=False)
    address2 = db.Column(db.String(100), nullable=False)
    suburb = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    item_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviews = db.relationship('Review', backref='order', lazy=True)

    def __repr__(self):
        return f"Order('{self.id}', '{self.item_id}', '{self.date_posted}')"

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ranking = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    item_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)

    def __repr__(self):
        return f"Review('{self.id}', '{self.ranking}', '{self.date_posted}')"