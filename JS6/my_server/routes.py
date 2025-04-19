from my_server import app
from flask import render_template, request
import json

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/addoneyear', methods=['POST', 'GET'])
def add_one_year():
    person = request.get_json()
    
    person['ålder'] += 1
    
    return json.dumps(person, indent=4)
    