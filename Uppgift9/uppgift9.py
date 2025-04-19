from flask import Flask, render_template
app = Flask(__name__)

@app.route("/minakompisar")
def mina_kompisar():
    kompisar = {"Joel", "Filip", "Leo"}
    return render_template("kompisar.html", kompisar=kompisar)

if __name__=='__main__':
    app.run(host="localhost", port=8080, debug=True)