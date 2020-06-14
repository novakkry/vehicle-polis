from flask import render_template, url_for, flash, redirect, flash, redirect, request
from marketplace import app, db, bcrypt
from marketplace.forms import RegistrationForm, LoginForm, PostForm
from marketplace.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import os
import secrets

@app.route("/")
@app.route("/home", methods=['GET','POST'])
def home():
    posts = Post.query.order_by(Post.id.desc()).all()
    posts_first = posts[:4]
    posts_second = posts[4:8]
    return render_template('home.html', posts=posts)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Account successfuly created.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    if current_user.is_authenticated: #this verification doesn't have to be here - I did it before I knew about @login_required
        return render_template('account.html')
    else: 
        return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    form_picture.save(picture_path)

    return picture_fn

@app.route("/add_item", methods=['GET','POST'])
@login_required
def add_item():
    form=PostForm()
    if current_user.role == 'buyer':
        flash('Only sellers can list cars.', 'info')
        return redirect(url_for('home'))
    else:
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                post = Post(image_file = picture_file, title = form.title.data, condition = form.condition.data, make = form.make.data, model = form.model.data, price = form.price.data, year = form.year.data, ODO = form.ODO.data, category = form.category.data, fuel = form.fuel.data, transmission = form.transmission.data, quantity = form.quantity.data, description = form.description.data, user_id = current_user.id)
            else:
                post = Post(title = form.title.data, condition = form.condition.data, make = form.make.data, model = form.model.data, price = form.price.data, year = form.year.data, ODO = form.ODO.data, category = form.category.data, fuel = form.fuel.data, transmission = form.transmission.data, quantity = form.quantity.data, description = form.description.data, user_id = current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Your car has been added!', 'success')
            return redirect(url_for('home'))
        return render_template('add_item.html', form=form)

@app.route("/item_list")
def item_list():
    posts = Post.query.order_by(Post.id.desc()).all()
    #posts = posts[1:2] limiting the selection
    return render_template('item_list.html', posts=posts)