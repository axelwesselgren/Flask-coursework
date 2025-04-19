from flask import render_template, session, redirect, url_for, flash, request
from server import app, bcrypt
from server.forms import RegisterForm, LoginForm, CreateThreadForm
from server.databasehandler import init_database, execute, get_item, get_tuple
from datetime import date
import json

init_database()

# Gör så att jag slipper kolla om användaren är inloggad på alla funktioner med samma kod
# Denna körs innan routsen så att de blir "skyddade"
@app.before_request
def require_login():
    protected_routes = ['member_area', 'create_thread', 'answer_thread', 'search_thread']

    if request.endpoint in protected_routes and not session.get('logged_in', False):
        flash("Not logged in", 'danger')
        return redirect(url_for('index'))
        

@app.route("/", methods=['POST', 'GET'])
@app.route("/index", methods=['POST', 'GET'])
def index():
    if session.get('logged_in', False):
        return redirect(url_for('member_area'))
    
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        
        user = get_item("SELECT id, username, hash FROM users WHERE username = ?", (username,))
        
        if not user:
            flash("User doesn't exist", 'danger')
            return redirect(url_for('index'))

        if not bcrypt.check_password_hash(user[2], password):
            flash("Incorrect password", 'danger')
            return redirect(url_for('index'))
        
        init_session(user[0], username)
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
    threads = get_tuple("SELECT title, content, id FROM posts WHERE parent_id IS NULL ORDER BY date ASC")
    return render_template('memberarea.html', logged_in=session.get('logged_in', False), username=session.get('username', ""), threads=threads)

@app.route('/logout')
def logout():
    pop_session()
    
    flash("Logged out", 'success')
    return redirect(url_for('index'))

@app.route("/createthread", methods=['GET', 'POST'])
def create_thread():
    form = CreateThreadForm()
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        
        create_thread(title, content, session['id'])
        return redirect(url_for('member_area'))
    
    return render_template('createthread.html', form=form, logged_in=session.get('logged_in', False))

@app.route("/answerthread/<thread_id>", methods=['GET', 'POST'])
def answer_thread(thread_id):
    if request.method == 'GET':
        thread = get_item("SELECT title, content FROM posts WHERE id = ?", (thread_id,))
        replies = get_tuple("SELECT title, content FROM posts WHERE parent_id = ?", (thread_id,))
        
        return render_template('answerthread.html', logged_in=session.get('logged_in', False), title=thread[0], thread_id=thread_id, content=thread[1], replies=replies)
    else:
        data = request.get_json()
        
        title = "RE:" + data['title']
        content = data['content']
        author_id = data['id']
        
        create_thread(title, content, author_id, parent_id=thread_id)
        return json.dumps({"status": "Success"}), 200


@app.route("/searchthread", methods=['GET', 'POST'])
def search_thread():
    if request.method == 'GET':
        return render_template('searchthread.html', logged_in=session.get('logged_in', False))
    else:
        data = request.get_json()
        search = data['search']
        offset = data['offset']
        
        results = get_tuple(
        """SELECT title, content FROM posts 
        WHERE LOWER(title) LIKE '%' || LOWER(?) || '%' 
        ORDER BY date ASC LIMIT 3 OFFSET ?""", (search, offset))
        return json.dumps({ "results": results }), 200

def init_session(idVal, username):
    session['logged_in'] = True
    session['id'] = idVal
    session['username'] = username

def pop_session():
    session.pop('logged_in')
    session.pop('username')
    session.pop('id')
    
def create_thread(title, content, author_id, date=date.today(), parent_id=None):
    execute("""
    INSERT INTO posts 
    (title, content, date, parent_id, author_id) 
    VALUES (?, ?, ?, ?, ?)""", (title, content, date, parent_id, author_id))