from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/hej")
def hej():
    username = "Axel"
    return render_template("hej.html", user=username)

@app.route("/date")
def date():
    date = datetime.now().date()
    return render_template("date.html", date=date)

if __name__=='__main__':
    app.run(host="localhost", port=8080, debug=True)