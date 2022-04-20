from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.chore import Chore
from flask import render_template, redirect, request, session, flash

@app.route('/')
def root():
    return render_template('index.html')

@app.errorhandler(404)
def error(incorrect):
    return 'So long, and thanks for all the fish!'