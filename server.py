from flask import Flask, escape, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Links(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(512))
    redir = db.Column(db.String(1024))
    metatitle = db.Column(db.String(512))
    metadesc = db.Column(db.String(512))
    metaurl = db.Column(db.String(512))
    metaimg = db.Column(db.String(512))

db.create_all()

@app.route('/', methods=["POST", "GET"])
def hello():
    if request.method == "POST":
        metatitle=None
        metadesc=None
        metaurl=None
        metaimg=None
        if request.form['metatitle']:
            metatitle = request.form['metatitle']
        else:
            metatitle=None
        if request.form['metadesc']:
            metadesc = request.form['metadesc']
        else:
            metadesc=None
        if request.form['metaurl']:
            metaurl = request.form['metaurl']
        else:
            metaurl=None
        if request.form['metaimg']:
            metaimg = request.form['metaimg']
        else:
            metaimg=None

        # haha bad code

        newLink = Links(link=request.form["weblink"], redir=request.form["link"], metatitle=metatitle, metadesc=metadesc, metaurl=metaurl, metaimg=metaimg)
        db.session.add(newLink)
        db.session.commit()
        return render_template("index.html", alert='Success! Link is https://go.jackmerrill.com/{0}').format(request.form["weblink"])
    return render_template("index.html")

@app.route("/<link>")
def goTo(link):
    checkLink = Links.query.filter_by(link=link).first()
    if not checkLink:
        return "Wrong link lol"
    return render_template("redir.html", metatitle=checkLink.metatitle, metadesc=checkLink.metadesc, metaurl=checkLink.metaurl, metaimg=checkLink.metaimg, redir=checkLink.redir)

@app.route("/api")
def api_base():
    return """
        I'm too lazy to make a webpage for this
        <br>
        DOCS:
        <br>
        /api/new - POST Request with headers:
        <br>
        shortlink*  -  The shortlink
        <br>
        url*  -  The URL to redirect to
        <br>
        metatitle|desc|url|img  -  Meta tags
        <br>
        * = required
    """

@app.route("/api/new", methods=["POST"])
def api_new():
    shortlink = request.headers["shortlink"]
    url = request.headers["url"]
    if request.headers['metatitle']:
        metatitle = request.headers['metatitle']
    else:
        metatitle=None
    if request.headers['metadesc']:
        metadesc = request.headers['metadesc']
    else:
        metadesc=None
    if request.headers['metaurl']:
        metaurl = request.headers['metaurl']
    else:
        metaurl=None
    if request.headers['metaimg']:
        metaimg = request.headers['metaimg']
    else:
        metaimg=None
    newLink = Links(link=shortlink, redir=url, metatitle=metatitle, metadesc=metadesc, metaurl=metaurl, metaimg=metaimg)
    db.session.add(newLink)
    db.session.commit()
    return "https://go.jackmerrill.com/{0}".format(shortlink)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6969, debug=True)