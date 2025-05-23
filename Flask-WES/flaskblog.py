import os
from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(32).hex()

posts = [
    {
        "author": "Axel Lonnby",
        "title": "Blog Post 1",
        "content": "First post content",
        "date_posted": "August 29, 2024"
    },
    {
        "author": "Axel Wesselgren",
        "title": "Blog Post 2",
        "content": "Second post content",
        "date_posted": "July 8, 2024"
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)