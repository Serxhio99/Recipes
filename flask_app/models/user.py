from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    
    db_name = 'recipes'
    
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        if results:
            for user in results:
                users.append( user )
            return users
        return users


    @classmethod
    def create_user(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update_user(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email= %(email)s WHERE id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_user(cls, data):
        query = "DELETE FROM users WHERE id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_user_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(user_id)s'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    @classmethod
    def get_user_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def delete_user_likes(cls, data):
        query = 'DELETE FROM likes WHERE user_id = %(user_id)s'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_user_recipes_likes(cls, data):
        query = """DELETE FROM likes WHERE recipe_id IN (SELECT id FROM recipes WHERE user_id = %(user_id)s);"""
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_like_by_userid(cls, data):
        query = 'SELECT * FROM likes WHERE user_id = %(user_id)s AND recipe_id = %(recipe_id)s'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    @staticmethod
    def validate_user(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailSignUp')
            is_valid = False
        if len(user['first_name'])< 3:
            flash('First name must be more than 2 characters', 'firstName')
            is_valid = False
        if len(user['last_name'])< 3:
            flash('Last name must be more than 2 characters', 'lastName')
            is_valid = False
        if len(user['password'])< 8:
            flash('Password must be more or equal to 8 characters', 'password')
            is_valid = False
        if user['confirm_password'] != user['password']:
            flash('The passwords do not match',  'passwordConfirm')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_user_update(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailSignUp')
            is_valid = False
        if len(user['first_name'])< 3:
            flash('First name must be more than 2 characters', 'firstName')
            is_valid = False
        if len(user['last_name'])< 3:
            flash('Last name must be more than 2 characters', 'lastName')
            is_valid = False
        return is_valid