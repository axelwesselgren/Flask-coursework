from flask import Flask, render_template, request, url_for, redirect
app = Flask(__name__)

@app.route("/start")
def start():
    return render_template("start.html")

@app.route("/memberarea")
def member_area():
    return render_template("memberarea.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    user = request.form["username"]
    password = request.form["password"]

    if user == "admin" and password == "123":
        return redirect(url_for('member_area'))

if __name__=='__main__':
    app.run(host="localhost", port=8080, debug=True)