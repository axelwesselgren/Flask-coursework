from flask import render_template, request
from my_server import app
from my_server.dbhandler import create_connection
import json

@app.route('/')
@app.route('/index/')
def start():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    
    department = data['department']
    search = data['search']
    
    search_result = []
    
    conn = create_connection()
    cur = conn.cursor()
    
    if department == 'all':
        cur.execute("SELECT namn, telefon, lon FROM anstalld WHERE LOWER(namn) LIKE LOWER(?) || '%'", (search,))
        search_result = cur.fetchall()
    else:
        cur.execute("SELECT namn, telefon, lon FROM anstalld WHERE LOWER(avdelning) = ?", (department,))
        search_result = cur.fetchall()
    
    cur.close()
    conn.close()
    
    search_dic = {
        'result': search_result
    }
    
    return json.dumps(search_dic, indent=4)