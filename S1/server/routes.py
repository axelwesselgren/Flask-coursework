from flask import render_template, session, redirect, url_for, flash
from server import app, bcrypt
from server.forms import RegisterForm, LoginForm
from server.databasehandler import init_database, execute, get_item

init_database()

@app.route("/", methods=['POST', 'GET'])
@app.route("/index", methods=['POST', 'GET'])
def index():
    if session.get('logged_in', False):
        return redirect(url_for('member_area'))
    
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        
        user = get_item("SELECT username, hash FROM users WHERE username = ?", (username,))
        
        if not user:
            flash("User doesn't exist", 'danger')
            return redirect(url_for('index'))

        if not bcrypt.check_password_hash(user[1], password):
            flash("Incorrect password", 'danger')
            return redirect(url_for('index'))
        
        session['logged_in'] = True
        session['username'] = username
        flash("Logged in successfully", 'success')
        return redirect(url_for('index'))
         
    return render_template('index.html', form=login_form, logged_in=session.get('logged_in', False))

@app.route('/createuser', methods=['POST', 'GET'])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        username = register_form.username.data
        password = register_form.password.data
        
        if get_item("SELECT username FROM users WHERE username = ?", (username,)):
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        
        hash = bcrypt.generate_password_hash(password)
        
        execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash))
        
        flash("Created user", 'success')
        return redirect(url_for('register'))

    return render_template('createuser.html', form=register_form, logged_in=session.get('logged_in', False))

@app.route('/memberarea')
def member_area():
    if not session.get('logged_in', False):
        flash("Not logged in", 'danger')
        return redirect(url_for('index'))
    return render_template('memberarea.html', logged_in=session.get('logged_in', False), username=session.get('username', ""))

@app.route('/logout')
def logout():
    if not session.get('logged_in', False):
        flash("Not logged in", 'danger')
        return redirect(url_for('index'))
    
    session.pop('logged_in')
    session.pop('username')
    
    flash("Logged out", 'success')
    return redirect(url_for('index'))