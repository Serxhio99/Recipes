from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    
    db_name = 'recipes'
    
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.u30 = data['u30']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_recipe_by_id(cls, data):
        query = 'SELECT * FROM recipes WHERE id= %(recipe_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    @classmethod
    def get_all(cls):
        query = """
                SELECT r.*, CONCAT(u.first_name, ' ', u.last_name) AS creator_name, 
                IFNULL(l.like_count, 0) AS like_count
                FROM recipes r
                LEFT JOIN users u ON r.user_id = u.id
                LEFT JOIN (
                    SELECT recipe_id, COUNT(*) AS like_count
                    FROM likes
                    GROUP BY recipe_id
                ) l ON r.id = l.recipe_id """
        results = connectToMySQL(cls.db_name).query_db(query)
        recipes = []
        if results:
            for recipe in results:
                recipes.append( recipe )
            return recipes
        return recipes
    
    @classmethod
    def get_all_user_recipes(cls, data):
        query = """
    SELECT r.*, u.first_name, u.last_name, COUNT(l.id) AS like_count
    FROM recipes r
    LEFT JOIN users u ON r.user_id = u.id
    LEFT JOIN likes l ON r.id = l.recipe_id
    WHERE r.user_id = %(user_id)s
    GROUP BY r.id;"""
        results = connectToMySQL(cls.db_name).query_db(query, data)
        recipes = []
        if results:
            for recipe in results:
                recipes.append( recipe )
            return recipes
        return recipes
    
    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date, u30, user_id) VALUES ( %(name)s, %(description)s, %(instructions)s , %(date)s, %(u30)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s , instructions = %(instructions)a, date = %(date)s, u30 = %(u30)s, user_id= %(user_id)s  WHERE id = %(recipe_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(recipe_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_all_user_recipes(cls, data):
        query = "DELETE FROM recipes WHERE user_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_recipe_like(cls, data):
        query = 'DELETE FROM likes WHERE recipe_id = %(recipe_id)s'
        return connectToMySQL(cls.db_name).query_db(query, data)

    
    @classmethod
    def like_recipe(cls, data):
        query = 'INSERT INTO likes (user_id, recipe_id) VALUES (%(user_id)s, %(recipe_id)s)'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def unlike_recipe(cls, data):
        query = 'DELETE FROM likes WHERE user_id = %(user_id)s AND recipe_id = %(recipe_id)s'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_all_recipe_likes(cls, data):
        query = "SELECT COUNT(*) AS like_count FROM likes WHERE recipe_id = %(recipe_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return 0
    
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        
        if len(recipe['name'])< 3:
            flash('Name must be more than 3 characters', 'recipeName')
            is_valid = False
        if len(recipe['description'])< 50:
            flash('recipe description must be more than 50 characters', 'recipeDesc')
            is_valid = False
        if len(recipe['instructions'])< 50:
            flash('recipe instructions must be more than 50 characters', 'recipeInstructions')
            is_valid = False
        if not recipe['date']:
            flash('Date is required', 'recipeDate')
            is_valid = False
        if  recipe['u30'] == 0:
            flash('Are 30 minutes enough', 'recipe30')
        return is_valid