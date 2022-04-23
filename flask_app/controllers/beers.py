from flask_app import app
from flask_app.models import user, beer, rating
from flask import render_template, redirect, request, session, flash

# Route to show the add beer form..
@app.route('/beer/add')
def add_beer_page():
    if 'user_id' not in session:
        return redirect('/login')

    # Styles dictionary for dropdown menu
    styles = {
        'Altbier': 'Altbier',
        'Amber ale': 'Amber ale',
        'Barley wine': 'Barley wine',
        'Berliner Weisse': 'Berliner Weisse',
        'Bière de Garde': 'Bière de Garde',
        'Bitter': 'Bitter',
        'Blonde Ale': 'Blonde Ale',
        'Bock': 'Bock',
        'Brown ale': 'Brown ale',
        'California Common/Steam Beer': 'California Common/Steam Beer',
        'Cream Ale': 'Cream Ale',
        'Doppelbock': 'Doppelbock',
        'Dunkel': 'Dunkel',
        'Dunkelweizen': 'Dunkelweizen',
        'Eisbock': 'Eisbock',
        'Fruit beer': 'Fruit beer',
        'Golden/Summer ale': 'Golden/Summer ale',
        'Gose': 'Gose',
        'Gueuze': 'Gueuze',
        'Hefeweizen': 'Hefeweizen',
        'Helles': 'Helles',
        'Herb and spiced beer': 'Herb and spiced beer',
        'Honey beer': 'Honey beer',
        'India pale ale': 'India pale ale',
        'Kölsch': 'Kölsch',
        'Lambic': 'Lambic',
        'Light ale':'Light ale',
        'Lager': 'Lager',
        'Maibock/Helles bock': 'Maibock/Helles bock',
        'Oktoberfestbier/Märzenbier': 'Oktoberfestbier/Märzenbier',
        'Old ale': 'Old ale',
        'Pale ale': 'Pale ale',
        'Pilsner': 'Pilsner',
        'Porter': 'Porter',
        'Red ale': 'Red ale',
        'Rye Beer': 'Rye Beer',
        'Saison': 'Saison',
        'Schwarzbier': 'Schwarzbier',
        'Scotch ale': 'Scotch ale',
        'Smoked beer': 'Smoked beer',
        'Stout': 'Stout',
        'Weissbier': 'Weissbier',
        'Weizenbock': 'Weizenbock',
        'Wild beer': 'Wild beer',
        'Witbier': 'Witbier',
        'Wood-aged beer': 'Wood-aged beer'
    }
    return render_template('add_beer.html',title = "Add Beer", styles = styles)


# Route to validate and add beer to database. redirects to show the beer that was just added.
@app.route('/beer/save-to-db', methods=['POST'])
def save_beer():
    if 'user_id' not in session:
        return redirect('/login')
    elif not beer.Beer.validate_beer(request.form):
        return redirect('/beer/add')
    else:
        data = {
            'user_id': session['user_id'],
            'name': request.form['name'],
            'brewery': request.form['brewery'],
            'style': request.form['style'],
            'ABV': request.form['ABV'],
            'IBU': request.form['IBU'],
        }
        new_beer_id = beer.Beer.save_beer(data)
        return redirect(f"/beer/{new_beer_id}/view")

# Route to show a single beer with it's ratings.
@app.route('/beer/<int:id>/view')
def show_beer(id):
    if 'user_id' not in session:
        return redirect('/login')
    data = {
        'id': id,
        'beer_id': id
    }
    one_beer = beer.Beer.get_beer_by_beer_id(data)
    one_beer_ratings = rating.Rating.get_all_rating_and_comments_by_beer_id(data)
    return render_template("show_beer.html", one_beer = one_beer, one_beer_ratings = one_beer_ratings)

# Route to favorite add beer to database. Place beer id in the route on front end
@app.route('/beer/<int:beer_id>/favorite', methods=['POST'])
def favorite_beer(beer_id):
    if 'user_id' not in session:
        return redirect('/login')
    data = {
        'user_id': session['user_id'],
        'beer_id': beer_id
    }
    beer.Beer.save_favorite(data)
    return redirect('/dashboard')
