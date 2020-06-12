from flask import render_template, url_for, flash, redirect, flash, redirect
from marketplace import app
from marketplace.forms import RegistrationForm, LoginForm

@app.route("/")
@app.route("/home", methods=['GET','POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('home.html', form=form)

@app.route("/add_edit_item")
def add_edit_item():
    return render_template('add_edit_item.html')

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account successfuly created for {form.username.data}.', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)
