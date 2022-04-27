from flask_app import app
from flask_app.models import user, rating
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Beer:
    schema_name = "beers_schema"

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.brewery = data['brewery']
        self.style = data['style']
        self.ABV = data['ABV']
        self.IBU = data['IBU']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        self.average_rating = None
        self.ratings = []
        self.favorite_id = None


    @staticmethod
    def validate_beer(beer):
        is_valid = True
        query = "SELECT * FROM beers WHERE beers.id = %(beer_id)s"
        results = connectToMySQL("beers_schema").query_db(query, beer)
        if len(beer['name']) < 2:
            flash("The name of the beer must be at least 2 characters", "beer")
            is_valid = False
        if len(beer['brewery']) < 2:
            flash("The brewery of the beer must be at least 2 characters", "beer")
            is_valid = False
        if len(beer['style']) < 2:
            flash("The style of the beer must be at least 2 characters", "beer")
            is_valid = False
            # need to change ABV and IBU to also include looking for it to be INT along with length???
        if len(beer['ABV']) < 1:
            flash("The ABV of the beer must be at least 1 characters", "beer")
            is_valid = False
        if len(beer['IBU']) < 2:
            flash("The IBU of the beer must be at least 2 characters", "beer")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_favorite(data):
        is_valid = True
        query = "SELECT * FROM favorites WHERE user_id = %(user_id)s AND beer_id = %(beer_id)s;"
        result = connectToMySQL("beers_schema").query_db(query, data)
        if len(result) > 0:
            is_valid = False
        return is_valid

    
    @classmethod
    def save_beer(cls, data):
        query = "INSERT INTO beers (user_id, name, brewery, style, ABV, IBU) VALUES (%(user_id)s, %(name)s, %(brewery)s, %(style)s, %(ABV)s, %(IBU)s);"
        return connectToMySQL("beers_schema").query_db(query, data)

    @classmethod
    def save_favorite(cls, data):
        query = "INSERT INTO favorites (user_id, beer_id) VALUES (%(user_id)s, %(beer_id)s);"
        return connectToMySQL("beers_schema").query_db(query, data)
    
    @classmethod
    def remove_favorite(cls, data):
        query = "DELETE FROM favorites WHERE id = %(id)s;"
        return connectToMySQL("beers_schema").query_db(query, data)
        
    @classmethod
    def get_all_beers(cls):
        query = "SELECT * FROM beers;"
        results = connectToMySQL('beers_schema').query_db(query)
        beers = []
        for row in results:
            beers.append(cls(row))
        return beers

    @classmethod
    def get_beer_by_beer_id(cls, data):
        query = "SELECT * FROM beers WHERE beers.id = %(id)s;"
        results = connectToMySQL('beers_schema').query_db(query, data)
        this_beer = cls(results[0])
        return this_beer

    @classmethod
    def get_all_beers_by_user_id(cls, data):
        query = "SELECT * FROM beers JOIN users ON users.id = beers.user_id WHERE users.id = %(user_id)s;"
        results = connectToMySQL("beers_schema").query_db(query, data)
        beers = []
        for row in results:
            beer_instance = cls(row)
            beer_data = {
                "user_id" : row['users.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'], 
                "age" : row['age'],
                "id" : row["id"],
                "name" : row['name'],
                "brewery" : row['brewery'],
                "style" : row['style'],
                "ABV" : row['ABV'],
                "IBU" : row['IBU'],
            }
            beers.append(beer_data)
        return beers

    @classmethod
    def get_all_beers_with_average_rating(cls):
        query = "SELECT avg(rating) as average_rating, beers.id, beers.user_id, beers.name, beers.brewery, beers.style, beers.ABV, beers.IBU, beers.created_at, beers.updated_at FROM beers LEFT JOIN ratings ON beers.id = ratings.beer_id GROUP BY beers.id;"
        results = connectToMySQL("beers_schema").query_db(query)
        if len(results) == 0:
            return None
        beers_with_average_rating = []
        for row in results:
            beer_data = {
                'id': row['id'],
                'user_id': row['user_id'],
                'name': row['name'],
                'brewery': row['brewery'],
                'style': row['style'],
                'ABV': row['ABV'],
                'IBU': row['IBU'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
            }
            beer_instance = cls(beer_data)
            beer_instance.average_rating = row['average_rating']
            beers_with_average_rating.append(beer_instance)
        return beers_with_average_rating

    # Get Beer with average rating
    @classmethod
    def get_one_beer_with_average_rating(cls, data):
        query = "SELECT avg(rating) as average_rating, beers.id, beers.user_id, beers.name, beers.brewery, beers.style, beers.ABV, beers.IBU, beers.created_at, beers.updated_at FROM beers LEFT JOIN ratings ON beers.id = ratings.beer_id WHERE beers.id = %(id)s GROUP BY beers.id;"
        result = connectToMySQL("beers_schema").query_db(query, data)
        this_beer = cls(result[0])
        for row in result:
            average_data = {
                'average_rating': row['average_rating']
            }
            this_beer.average_rating = average_data['average_rating']
        return this_beer

    # Get 1 beer with all ratings and user
    @classmethod
    def get_one_beer_with_user_all_ratings(cls, data):
        query = "SELECT * FROM beers LEFT JOIN ratings ON beers.id = ratings.beer_id LEFT JOIN users ON ratings.user_id = users.id WHERE beers.id = %(id)s;"
        results = connectToMySQL("beers_schema").query_db(query, data)
        print(results)
        this_beer = cls(results[0])
        for row in results:
            rating_data = {
                'id': row['ratings.id'],
                'user_id': row['user_id'],
                'beer_id': row['beer_id'],
                'rating': row['rating'],
                'comment': row['comment'],
                'created_at': row['ratings.created_at'],
                'updated_at': row['ratings.updated_at'],
            }
            one_rating=rating.Rating(rating_data)
            user_rating_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'age': row['age'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            one_rating.user = user.User(user_rating_data)
            this_beer.ratings.append(one_rating)
        return this_beer


    # Moved to user model Currently being used on dashboard
    @classmethod
    def get_all_favorited_beers_by_user_id(cls, data):
        query = "SELECT * FROM favorites JOIN users ON users.id = favorites.user_id JOIN beers ON beers.id = favorites.beer_id WHERE users.id = %(user_id)s;"
        results = connectToMySQL("beers_schema").query_db(query, data)
        if len(results) == 0:
            return None
        beers = []
        for row in results:
            beer_instance = cls(row)
            beer_data = {
                "user_id" : row['users.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'], 
                "age" : row['age'],
                "beer_id" : row["beers.id"],
                "name" : row['name'],
                "brewery" : row['brewery'],
                "style" : row['style'],
                "ABV" : row['ABV'],
                "IBU" : row['IBU'],
            }
            beers.append(beer_data)
        return beers



