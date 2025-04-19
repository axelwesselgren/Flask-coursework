from flask import render_template
from my_server import app

@app.errorhandler(401)
def unathoriazed_error(error):
    return render_template('errors/401.html'), 401

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404