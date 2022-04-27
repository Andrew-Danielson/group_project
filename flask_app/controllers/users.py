from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import user, beer

from flask import render_template, redirect, request, session, flash

# Route to Show Landing Page
@app.route('/')
def root():
    return render_template('index.html')

# Route to show login page
@app.route('/login')
def login_page():
    return render_template('login.html')

# Route to validate user login and login user
@app.route('/login_to_app', methods =['POST'])
def login_to_app():
    data = {
        "email": request.form["email"]
    }
    user_in_db = user.User.get_user_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid Email/Password")
        return redirect('/login')
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    return redirect("/dashboard")

# Route to display dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id': session['user_id'],
            'user_id': session['user_id']
        }
        this_user = user.User.get_user_with_favorite_beers(data)
        all_beers = beer.Beer.get_all_beers_with_average_rating()
    return render_template('dashboard.html', all_beers = all_beers, this_user = this_user)

# Route to show user registration page
@app.route('/register')
def register():
    return render_template('register.html')

# Route to Register a new user
@app.route('/register_user', methods=['POST'])
def register_user():
    if not user.User.validate_user(request.form):
        return redirect ('/')
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'age': request.form['age'],
            'password': pw_hash,
        }
        user_id = user.User.save_user(data)
        session['user_id'] = user_id
        session['first_name'] = request.form['first_name']
        return redirect('/dashboard')

# Route to display user account

@app.route('/my-account')
def my_account():
    if 'user_id' not in session:
        return redirect('/login')
    else:
        data={
            'user_id': session['user_id']
        }
        this_user = user.User.get_user_with_favorite_beers(data)
        return render_template('my-account.html', this_user = this_user)

# Route to edit user profile
@app.route('/edit-account', methods=['POST'])
def edit_account():
    if 'user_id' not in session:
        return redirect('/login')
    if not user.User.validate_user(request.form):
        return redirect ('/')
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            'user_id': session['user_id'],
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash,
        }
        user.User.update_user(data)
        return redirect('/my-account')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.errorhandler(404)
def error(incorrect):
    return 'So long, and thanks for all the fish!'