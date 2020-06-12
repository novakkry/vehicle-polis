from flask import render_template, url_for, flash, redirect
from marketplace import app

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/add_edit_item")
def add_edit_item():
    return render_template('add_edit_item.html')