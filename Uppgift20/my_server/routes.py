from flask import abort, redirect, render_template, request, session, url_for, flash
from my_server.hardcoded_database import posts, users
from my_server.forms import LoginForm, PostForm, RegisterForm, SettingsForm
from my_server import app
from werkzeug.utils import secure_filename
import os

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html', logged_in=session.get('logged_in', False))

@app.route("/login", methods=['POST', 'GET'])
def login():
    if not session.get('logged_in', False):
        form = LoginForm()

        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            if not user_exists(username):
                flash('User does not exist', 'danger')
                return redirect(url_for('login'))
            
            for user in users:
                if username == user['username']:
                    if password == user['password']:
                        session['logged_in'] = True
                        session['username'] = username
                        session['id'] = get_id(username)
                        session['profile_picture'] = user['profile_picture']

                        flash('Sucessfully logged in', 'success')
                        return redirect(url_for('users_list'))
                    else:
                        flash('Wrong password', 'danger')
                        return redirect(url_for('login'))
                
        return render_template('login.html', form=form, logged_in=session.get('logged_in', False))
    else:
        flash('You are already logged in', 'danger')
        return redirect(url_for('index'))

@app.route("/users/<username>")
@app.route("/users")
def users_list(username=None):
    if session.get('logged_in', False):
        if username == None:
            return render_template('listusers.html', users=users, logged_in=session['logged_in'])
        else:
            posts_filtered = []
            id = get_id(username)
            for post in posts:
                if (id == post['author_id']):
                    posts_filtered.append(post)

            return render_template(
                'listposts.html', 
                posts=posts_filtered, 
                username=username, 
                logged_in=session['logged_in'], 
                pic = get_user(id)['profile_picture']
            )
    else:
        flash('You need login acces to view this page', 'danger')
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    if session.get('logged_in', False):
        session['logged_in'] = False
        session.pop('id')
        session.pop('username')
        session.pop('profile_picture')

        flash('Succesfully logged out', 'success')
    return redirect(url_for('index'))

@app.route("/create-post", methods=['POST', 'GET'])
def create_post():
    if session.get('logged_in', False):
        form = PostForm()
        if form.validate_on_submit():
            posts.append(
                {
                    'id' : os.urandom(32).hex(),
                    'author_id' : session['id'],
                    'content' : form.content.data
                }
            )
            return redirect(url_for('users_list', username=session['username']))
        return render_template('createpost.html', logged_in=session.get('logged_in', False), form=form)
    else:
        flash('You need login access to view this page', 'danger')
        return redirect(url_for('login'))

@app.route("/create-user", methods=['POST', 'GET'])
def create_user():
    if not session.get('logged_in', False):
        form = RegisterForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            id = os.urandom(32).hex()

            if user_exists(username):
                flash('User already exists', 'danger')
                return redirect(url_for('create_user'))

            if password != form.confirm_password.data:
                flash('Passwords must match!', 'danger')
                return redirect(url_for('create_user'))
            
            users.append(
                {
                    'id' : id,
                    'username' : username,
                    'password' : password,
                    'profile_picture' : 'default.jpg'
                }
            )

            session['username'] = username
            session['logged_in'] = True
            session['id'] = id
            session['profile_picture'] = "default.jpg"

            flash('Succesfully created user', 'success')
            return redirect(url_for('users_list'))

        return render_template('createaccount.html', logged_in=session.get('logged_in', False), form=form)
    else:
        flash('You are logged in, log out to create an account', 'danger')
        return redirect(url_for('index'))
    
@app.route("/settings", methods=['POST', 'GET'])
def settings():
    if session.get('logged_in', False):
        form = SettingsForm()

        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            user = get_user(session['id'])
            user['username'] = username
            user['password'] = password

            session['username'] = username

            f = form.upload.data
            if f:
                filename = secure_filename(f.filename)
                f.save(os.path.join(
                    app.root_path, 
                    'static', 
                    'images', 
                    'profile_pictures',
                    filename
                ))

                user['profile_picture'] = filename
                session['profile_picture'] = filename
            
            flash('Succesfully changed settings', 'success')
            return redirect(url_for('settings'))
            
        return render_template(
            'settings.html', 
            logged_in=session['logged_in'], 
            form=form, 
            pic = session['profile_picture']
        )

    else: abort(401)

def get_id(username):
    for user in users:
        if username == user['username']:
            return user['id']
        
def user_exists(username):
    for user in users:
        if username == user['username']:
            return True
    return False

def get_user(id):
    for user in users:
        if id == user['id']:
            return user
