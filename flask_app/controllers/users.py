from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# Intro
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return redirect('/logout')

# LOAD LOG IN PAGE
@app.route('/loginPage')
def loginPage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('login.html')

# LOAD REGISTER PAGE
@app.route('/registerPage')
def registerPage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('register.html')

# CONTROL LOG IN FORM
@app.route('/login', methods = ['POST'])
def login():
    if 'user_id' in session:
        return redirect('/')
    user = User.get_user_by_email(request.form)
    if not user:
        flash('This email does not exist.', 'LogEmail')
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash('Your password is wrong!', 'passLog')
        return redirect(request.referrer)
    session['user_id'] = user['id']
    return redirect('/')

#  CONTROL REGISTER FORM
@app.route('/register', methods= ['POST'])
def register():
    if 'user_id' in session:
        return redirect('/')
    
    if User.get_user_by_email(request.form):
        flash('This email already exists. Try another one.', 'emailSignUp')
        return redirect(request.referrer)
    
    if not User.validate_user(request.form):
        return redirect(request.referrer)
    
    data = {
        'first_name': request.form.get('first_name'),
        'last_name': request.form.get('last_name'),
        'email': request.form.get('email'),
        'password': bcrypt.generate_password_hash(request.form.get('password')),
        'confirm_password': request.form.get('confirm_password')
    }
    
    User.create_user(data)
    flash('User succefully created', 'userRegister')
    return redirect('/')

# LOAD DASHBOARD
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    loggedUserData = {
        'user_id': session['user_id']
    } 
    loggedUser = User.get_user_by_id(loggedUserData)
    if not loggedUser:
        return redirect('/logout')
    return render_template('dashboard.html', recipes = Recipe.get_all(), loggedUser = User.get_user_by_id(loggedUserData), users = User.get_all())

# LOAD PROFILE
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/')
    loggedUserData = {
        'user_id': session['user_id']
    }
    noRecipes = len(Recipe.get_all_user_recipes(loggedUserData))
    return render_template('profile.html',loggedUser = User.get_user_by_id(loggedUserData), recipes=Recipe.get_all_user_recipes(loggedUserData),noRecipes = noRecipes)

#  LOAD EDIT PROFILE
@app.route('/edit/profile')
def editProfile():
    if 'user_id' not in session:
        return redirect('/')
    loggedUserData = {
        'user_id': session['user_id']
    }
    return render_template('editProfile.html',loggedUser = User.get_user_by_id(loggedUserData))

# CONTROL EDIT PROFILE FORM
@app.route('/edit/user/profile', methods = ['POST'])
def editUserProfile():
    if 'user_id' not in session:
        return redirect('/')
    if not User.validate_user_update(request.form):
        return redirect(request.referrer)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'user_id': session['user_id']
    }
    loggedUser = User.get_user_by_id(data)
    if loggedUser['id'] == session['user_id']:
        User.update_user(data)
        flash('User succesfully updated!', 'succesfulUpdate')
        return redirect('/profile')
    return redirect(request.referrer)


# DELETE PROFILE
@app.route('/delete/profile')
def deleteProfile():
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'user_id': session['user_id']
    }
    loggedUser = User.get_user_by_id(data)
    if loggedUser['id'] == session['user_id']:
        User.delete_user_likes(data)
        User.delete_user_recipes_likes(data)
        Recipe.delete_all_user_recipes(data)
        User.delete_user(data)
        return redirect('/logout')
    return redirect(request.referrer)

# CONTROL LOG OUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/loginPage')