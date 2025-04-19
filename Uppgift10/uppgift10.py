from flask import Flask, render_template
app = Flask(__name__)

@app.route("/user/<name>/<surname>")
@app.route("/user/<name>")
@app.route("/user")
def user(name=None, surname=None):
    return render_template("index.html", name=name, surname=surname)


if __name__=='__main__':
    app.run(host="localhost", port=8080, debug=True)