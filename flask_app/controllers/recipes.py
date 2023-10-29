from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_app.models.user import User
from flask_app.models.recipe import Recipe


# LOAD CREATE RECIPE
@app.route('/recipes/new')
def addrecipe():
    if 'user_id' not in session:
        return redirect('/')
    loggedUserData = {
        'user_id': session['user_id']
    }
    return render_template('addRecipe.html', loggedUser=User.get_user_by_id(loggedUserData))


# CONTROL ADD RECIPE FORM
@app.route('/addRecipe', methods=['POST'])
def createrecipe():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect(request.referrer)
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date': request.form['date'],
        'u30': request.form.get('u30'),
        'user_id': session['user_id']   
    }   
    Recipe.create_recipe(data)
    return redirect('/dashboard')


# VIEW RECIPE
@app.route('/recipes/<int:id>')
def viewRecipe(id):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'user_id': session['user_id'],
        'recipe_id': id
    }
    loggedUser = User.get_user_by_id(data)
    recipe = Recipe.get_recipe_by_id(data)
    likes = Recipe.get_all_recipe_likes(data)
    liked = User.get_like_by_userid(data)
    return render_template('recipe.html', recipe=recipe, loggedUser=loggedUser, likes=likes, liked=liked)


# LOAD EDIT RECIPE
@app.route('/recipes/edit/<int:id>')
def loadedit(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'recipe_id': id
    }
    loggedUser = User.get_user_by_id(data)
    recipe = Recipe.get_recipe_by_id(data)
    if loggedUser['id'] == recipe['user_id']:
        return render_template('editRecipe.html', recipe=recipe, loggedUser=loggedUser)
    return redirect(request.referrer)


# CONTROL EDIT RECIPE FORM
@app.route('/recipes/edit/<int:id>', methods=['POST'])
def editRecipe(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect(request.referrer)
    data = {
        'recipe_id': id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date': request.form['date'],
        'u30': request.form.get('u30'),
        'user_id': session['user_id']   
    }
    loggedUser = User.get_user_by_id(data)
    recipe = Recipe.get_recipe_by_id(data)
    if loggedUser['id'] == recipe['user_id']:
        Recipe.update_recipe(data)
    return redirect(f'/recipes/{id}')


# LIKE RECIPE
@app.route('/like/recipe/<int:id>')
def likeRecipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'recipe_id': id
    }
    loggedUser = User.get_user_by_id(data)
    recipe = Recipe.get_recipe_by_id(data)
    Recipe.like_recipe(data)
    return redirect(request.referrer)


# UNLIKE RECIPE
@app.route('/unlike/recipe/<int:id>')
def unlikeRecipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'recipe_id': id
    }
    loggedUser = User.get_user_by_id(data)
    recipe = Recipe.get_recipe_by_id(data)
    Recipe.unlike_recipe(data)
    redirect(request.referrer)
    return redirect(f'/recipes/{id}')


# DELETE RECIPE
@app.route('/delete/recipe/<int:id>')
def deleterecipe(id):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'user_id': session['user_id'],
        'recipe_id': id
    }
    loggedUser = User.get_user_by_id(data)
    recipe = Recipe.get_recipe_by_id(data)
    if loggedUser['id'] == recipe['user_id']:
        Recipe.delete_recipe_like(data)
        Recipe.delete_recipe(data)
        return redirect(request.referrer)
    return redirect(request.referrer)