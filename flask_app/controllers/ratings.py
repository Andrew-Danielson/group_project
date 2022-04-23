from flask_app import app
from flask_app.models import user, beer, rating
from flask import render_template, redirect, request, session, flash

# Route to show the rating beer page
@app.route('/beer/<int:id>/rate')
def rate_beer_page(id):
    data = {
        'id': id
    }
    one_beer = beer.Beer.get_beer_by_beer_id(data)
    return render_template('rate_beer.html', one_beer = one_beer)

# Route to add rating to database. Redirects back to dashboard
@app.route('/rating/save-to-db')
def save_rating():
    if 'user_id' not in session:
        return redirect('/login')
    elif not rating.Rating.validate_raiting(request.form):
        return redirect(f"/beer/{request.form['beer_id']}/rate")
    else:
        data = {
            'user_id': session['user_id'],
            'beer_id': request.form['beer_id'],
            'rating': request.form['brewery'],
            'comment': request.form['comment'],
        }
        new_rating_id = rating.Rating.save_rating(data)
        return redirect('/dashboard')