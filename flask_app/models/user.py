from urllib import request
from flask_app import app
from flask_app.models import beer, rating
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime, date
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    schema_name = "beers_schema"

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.age = data['age']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.beers = []
        self.favorite_beers = []

    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("beers_schema").query_db(query, user)
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.", "registration")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.", "registration")
            is_valid = False
        print(user)
        if 'age' in user:
            # Calculate Age of User
            date_object = datetime.strptime(user['age'],'%Y-%m-%d').date()
            def age(birthdate):
                today = date.today()
                age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
                return age
            print(user['age'])
            # Validate age
            if  age(date_object) < int(21):
                flash("You must be 21 or older to enter this site", "registration")
        if len(results) >= 1:
            flash("Email already taken.", "registration")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", "registration")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", "registration")
            is_valid = False
        if user["password"] != user["confirm_password"]:
            flash("Passwords must match", "registration")
            is_valid = False
        return is_valid

    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, age, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(age)s, %(password)s);"
        return connectToMySQL("beers_schema").query_db(query, data)
    
    @classmethod
    def update_user(cls, data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, password=%(password)s WHERE users.id = %(user_id)s;"
        return connectToMySQL("beers_schema").query_db(query, data)

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("beers_schema").query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL("beers_schema").query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('beers_schema').query_db(query)
        users = []
        for entry in results:
            users.append(cls(entry))
        return users

    # Get User with favorite beers
    @classmethod
    def get_user_with_favorite_beers(cls, data):
        query = "SELECT * FROM users LEFT JOIN favorites ON users.id = favorites.user_id LEFT JOIN beers on favorites.beer_id = beers.id WHERE users.id = %(user_id)s;"
        results = connectToMySQL("beers_schema").query_db(query, data)
        this_user = cls(results[0])
        for row_in_db in results:
            beer_data = {
                'id': row_in_db['beers.id'],
                'user_id': row_in_db['beers.user_id'],
                'name': row_in_db['name'],
                'brewery': row_in_db['brewery'],
                'style': row_in_db['style'],
                'ABV': row_in_db['ABV'],
                'IBU': row_in_db['IBU'],
                'created_at': row_in_db['beers.created_at'],
                'updated_at': row_in_db['beers.updated_at'],
            }
            beer_instance = beer.Beer(beer_data)
            beer_instance.favorite_id = row_in_db['favorites.id']
            this_user.favorite_beers.append(beer_instance)
        return this_user

