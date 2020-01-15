from flask import Flask, escape, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Links(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(512))
    redir = db.Column(db.String(1024))

db.create_all()

@app.route('/', methods=["POST", "GET"])
def hello():
    if request.method == "POST":
        newLink = Links(link=request.form["weblink"], redir=request.form["link"])
        db.session.add(newLink)
        db.session.commit()
        return render_template("index.html", alert='Success! Link is https://go.jackmerrill.com/{0}').format(request.form["weblink"])
    return render_template("index.html")

@app.route("/<link>")
def goTo(link):
    checkLink = Links.query.filter_by(link=link).first()
    if not checkLink:
        return "Wrong link lol"
    return redirect(checkLink.redir)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6969, debug=False)