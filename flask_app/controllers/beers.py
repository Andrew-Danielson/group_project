from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.beer import Beer
from flask import render_template, redirect, request, session, flash


@app.route('/add/beer')
def add_beer():
    return render_template('add_beer.html',title = "Add Beer")