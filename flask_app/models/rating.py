from flask_app import app
from flask_app.models import user, beer
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Rating:
    schema_name = "beers_schema"

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.beer_id = data['beer_id']
        self.rating = data['rating']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.beer = []

    @staticmethod
    def validate_raiting(rating):
        is_valid = True
        query = "SELECT * FROM rating where rating.id = %(rating_id)s"
        results = connectToMySQL("beers_schema").query_db(query, rating)
        if rating['rating'] != int(min=0, max=10):
            flash("please select a number between 0 and 10", "rating")
            is_valid = False
        return is_valid

    @classmethod
    def save_rating(cls, data):
        query = "INSERT INTO rating (user_id, beer_id, rating, comment) VALUES (%(user_id)s, %(beer_id)s,%(rating)s,%(comment)s);"
        return connectToMySQL("beers_schema").query_db(query, data)

    @classmethod
    def get_all_rating_and_comments_by_beer_id(cls, data):
        query = "SELECT * FROM rating JOIN users ON users.id = rating.user_id JOIN beers ON beers.id = rating.beer_id WHERE beers.id = %(beer_id)s;"
        results = connectToMySQL("beers_schema").query_db(query, data)
        rating = []
        for row in results:
            rating_instance = cls(row)
            rating_data = {
                "user_id" : row['users.id'],
                "beer_id" : row['beers.id'],
                "rating" : row['rating'],
                "comment" : row['comment'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'], 
                "age" : row['age'],
                "name" : row['name'],
                "brewery" : row['brewery'],
                "style" : row['style'],
                "ABV" : row['ABV'],
                "IBU" : row['IBU'],
            }
            rating.append(rating_data)
        return rating

    @classmethod
    def get_all_rating_and_comments_by_user_id(cls, data):
        query = "SELECT * FROM rating JOIN users ON users.id = rating.user_id JOIN beers ON beers.id = rating.beer_id WHERE users.id = %(user_id)s;"
        results = connectToMySQL("beers_schema").query_db(query, data)
        rating = []
        for row in results:
            rating_instance = cls(row)
            rating_data = {
                "user_id" : row['users.id'],
                "beer_id" : row['beers.id'],
                "rating" : row['rating'],
                "comment" : row['comment'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'], 
                "age" : row['age'],
                "name" : row['name'],
                "brewery" : row['brewery'],
                "style" : row['style'],
                "ABV" : row['ABV'],
                "IBU" : row['IBU'],
            }
            rating.append(rating_data)
        return rating