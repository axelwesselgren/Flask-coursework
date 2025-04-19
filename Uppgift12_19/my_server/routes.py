from flask import session, abort, request, flash, redirect, url_for, render_template
from my_server import app

@app.route("/member")
def member():
    if 'logged_in' in session and session['logged_in']:
        return render_template("member.html")
    abort(401)

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == '123':
            flash("Du är nu inloggad", 'info')
            session['logged_in'] = True
            return redirect(url_for('member'))
        else:
            flash('Kontrollera ditt användarnamn och lösenord', 'warning')
            return redirect(url_for('login'))
    if 'logged_in' not in session:
        session['logged_in'] = False
    
    return render_template("login.html", logged_in=session['logged_in'])

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

if __name__=='__main__':
    app.run(debug=True, host="localhost", port=8080) 