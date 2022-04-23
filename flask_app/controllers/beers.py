from flask_app import app
from flask_app.models import user, beer
from flask import render_template, redirect, request, session, flash


@app.route('/add/beer')
def add_beer():
    return render_template('add_beer.html',title = "Add Beer")