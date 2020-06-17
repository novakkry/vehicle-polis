from flask import render_template, url_for, redirect, flash, redirect, request, abort
from marketplace import app, db, bcrypt
from marketplace.forms import RegistrationForm, LoginForm, PostForm, OrderForm, NumberRange, SearchForm, ReviewForm, HomeSearchForm
from marketplace.models import User, Post, Order, Review
from flask_login import login_user, current_user, logout_user, login_required
import os
import secrets

@app.route("/", methods=['GET','POST'])
@app.route("/home", methods=['GET','POST'])
def home():
    searchform = SearchForm()
    categorysearchform = HomeSearchForm()
    posts = Post.query.order_by(Post.id.desc()).all()
    posts_first = posts[:4] #latest 8 posts
    posts_second = posts[4:8]
    count = Post.query.count()
    if categorysearchform.validate_on_submit():
        price_to = 99999999999999
        year_from = 0
        year_to = 9999999
        odo_from = 0
        odo_to = 99999999999999
        if not categorysearchform.price_from.data:
            categorysearchform.price_from.data = 0
        if not categorysearchform.price_to.data:
            categorysearchform.price_to.data = 99999999999999
        if not categorysearchform.year_from.data:
            categorysearchform.year_from.data = 0
        if not categorysearchform.year_to.data:
            categorysearchform.year_to.data = 99999999999999
        if not categorysearchform.odo_from.data:
            categorysearchform.odo_from.data = 0
        if not categorysearchform.odo_to.data:
            categorysearchform.odo_to.data = 99999999999999

        posts = Post.query.order_by(Post.id.desc()).all()
        posts = Post.query.filter(Post.price >= categorysearchform.price_from.data, Post.price <= categorysearchform.price_to.data,\
        Post.year >= categorysearchform.year_from.data, Post.year <= categorysearchform.year_to.data,\
        Post.ODO >= categorysearchform.odo_from.data, Post.ODO <= categorysearchform.odo_to.data\
        ).order_by(Post.id.desc()).all()
        
        if categorysearchform.transmission.data:
            posts_transmission = Post.query.filter(Post.transmission == categorysearchform.transmission.data).all()
            posts = set(posts).intersection(set(posts_transmission))
        
        if categorysearchform.category.data:
            posts_category = Post.query.filter(Post.category == categorysearchform.category.data).all()
            posts = set(posts).intersection(set(posts_category))
        
        if categorysearchform.fuel.data:
            posts_fuel = Post.query.filter(Post.fuel == categorysearchform.fuel.data).all()
            posts = set(posts).intersection(set(posts_fuel))

    #*********************************finish cars filtering*********************************************

        if not posts:
            flash('There are no vehicles meeting your criteria. Sorry.', 'info')
            return render_template('home.html', posts_first=posts_first, posts_second=posts_second, count=count, searchform=searchform, categorysearchform=categorysearchform)

        return render_template('item_list.html', posts=posts, searchform=searchform)
        

    # if searchform.validate_on_submit():
    #     flash('Full text search form engaged', 'success')
    #     posts = Post.query.order_by(Post.id.desc()).all()
    #     return redirect(url_for('item_list'))
    
    return render_template('home.html', posts_first=posts_first, posts_second=posts_second, count=count, searchform=searchform, categorysearchform=categorysearchform)

@app.route("/login", methods=['GET','POST'])
def login():
    searchform = SearchForm()
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
    return render_template('login.html', form=form, searchform=searchform)

@app.route("/register", methods=['GET','POST'])
def register():
    searchform = SearchForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=form.role.data, contact_number=form.contact_number.data)
        db.session.add(user)
        db.session.commit()
        flash('Account successfuly created.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', searchform=searchform, title='Register', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    searchform = SearchForm()
    posts = Post.query.order_by(Post.id.desc()).filter(Post.author == current_user)
    orders = Order.query.order_by(Order.id.desc()).filter(Order.author == current_user)
    posts_count = Post.query.order_by(Post.id.desc()).filter(Post.author == current_user).count()
    orders_count = Order.query.order_by(Order.id.desc()).filter(Order.author == current_user).count()
    return render_template('account.html', searchform=searchform, posts=posts, orders=orders, posts_count=posts_count, orders_count=orders_count)

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
    searchform = SearchForm()
    form=PostForm()
    if current_user.role == 'buyer':
        flash('Only sellers can list cars.', 'info')
        return redirect(url_for('home'))
    else:
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                post = Post(image_file = picture_file, title = form.title.data, condition = form.condition.data, make = form.make.data, model = form.model.data, price = form.price.data, year = form.year.data, ODO = form.ODO.data, category = form.category.data, fuel = form.fuel.data, transmission = form.transmission.data, quantity = form.quantity.data, description = form.description.data, author = current_user)
            else:
                post = Post(title = form.title.data, condition = form.condition.data, make = form.make.data, model = form.model.data, price = form.price.data, year = form.year.data, ODO = form.ODO.data, category = form.category.data, fuel = form.fuel.data, transmission = form.transmission.data, quantity = form.quantity.data, description = form.description.data, author = current_user)
            db.session.add(post)
            db.session.commit()
            flash('Your car has been added!', 'success')
            return redirect(url_for('home'))
        return render_template('add_item.html', searchform=searchform, form=form, legend='Create a new listing')

@app.route("/item_list")
def item_list():
    searchform = SearchForm()
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('item_list.html', posts=posts, searchform=searchform)

@app.route("/item_details/<int:post_id>", methods=['GET','POST'])
def post(post_id):
    searchform = SearchForm()
    form = ReviewForm()
    post = Post.query.get_or_404(post_id)
    order = Order.query.order_by(Order.id.desc()).first() #ted to posila query na vsechny ordery a vubec se to nefiltruje. Zmenit!!!
    reviews = Review.query.filter(Review.item_id == post_id).order_by(Review.id.desc()).all()
    ordered = ''
    written = 1
    own = ''
    if current_user.is_authenticated:
        ordered = Order.query.filter(Order.item_id == post_id, Order.user_id == current_user.id).first()
        written = Review.query.filter(Review.user_id == current_user.id, Review.item_id == post_id).first()
        own = Post.query.filter(Post.user_id == current_user.id, Post.id == post_id).first()
    if form.validate_on_submit():
        review = Review(ranking=form.ranking.data, content=form.content.data, author=current_user, item=post, order=order)
        db.session.add(review)
        db.session.commit()
        reviews = Review.query.filter(Review.item_id == post_id).order_by(Review.id.desc()).all()
        flash('Your review was sucessfully posted!', 'success')
        return redirect(url_for('post', post_id=post_id))
    return render_template('item_details.html', searchform=searchform, title=post.title, post=post, form=form, reviews=reviews, ordered=ordered, written=written, own=own)

@app.route("/item_details/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
    searchform = SearchForm()
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.make = form.make.data
        post.condition = form.condition.data
        post.model = form.model.data
        post.price = form.price.data
        post.year = form.year.data
        post.ODO = form.ODO.data
        post.category = form.category.data
        post.fuel = form.fuel.data
        post.transmission = form.transmission.data
        post.description = form.description.data
        post.quantity = form.quantity.data
        db.session.commit()
        flash('Your listing has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.make.data = post.make
        form.condition.data = post.condition
        form.model.data = post.model
        form.price.data = post.price
        form.year.data = post.year
        form.ODO.data = post.ODO
        form.category.data = post.category
        form.fuel.data = post.fuel
        form.transmission.data = post.transmission
        form.quantity.data = post.quantity
        form.description.data = post.description
    return render_template('add_item.html', searchform=searchform, form=form, legend='Update listing')

@app.route("/item_details/<int:post_id>/delete", methods=['GET','POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your listing has been deleted!', 'info')
    return redirect(url_for('home'))

@app.route("/item_details/<int:post_id>/order", methods=['GET','POST'])
@login_required
def order_item(post_id):
    searchform = SearchForm()
    post = Post.query.get_or_404(post_id)
    form = OrderForm()
    maxquantity = post.quantity
    form.quantity.validators = [form.quantity.validators[0], NumberRange(min=1, max=maxquantity, message='Ordered quantity has to be no more than available quantity.')]
    if form.validate_on_submit():
        order = Order(date_posted = form.date_posted.data, quantity=form.quantity.data, first_name=form.first_name.data, last_name=form.last_name.data, company_name=form.company_name.data, address1=form.address1.data, address2=form.address2.data, suburb=form.suburb.data, city=form.city.data, state=form.state.data, country=form.country.data, phone=form.phone.data, email=form.email.data, author = current_user, item = post)
        db.session.add(order)
        db.session.commit()
        post.quantity = post.quantity-form.quantity.data
        db.session.commit()
        flash('Your order has been submitted!', 'info')
        return redirect(url_for('order_details', order_id=order.id))
    elif request.method == 'GET':
        form.email.data = current_user.email
    return render_template('order_item.html', searchform=searchform, post=post, form=form)

@app.route("/order_details/<int:order_id>", methods=['GET','POST'])
def order_details(order_id):
    searchform = SearchForm()
    order = Order.query.order_by(Order.id.desc()).filter(Order.id == order_id).first()
    if order.author != current_user:
        abort(403)
    return render_template('order_details.html', searchform=searchform, order=order)