from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#configure app
app = Flask(__name__)

#configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

# Import Movie data model, must be imported after db is set to prevent cyclic import conflict
from models import Movie, Theme

# Run server in debug mode (update when changes are made)
#app.run(debug=True)

# root webpage
@app.route("/")
def index():
    movies = Movie.query.order_by(Movie.title).all()
    return render_template("index.html", movies=movies)

# just used for post, adds data to database
# TODO add data through route instead of request
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    composer = request.form.get("composer")
    if not title or not composer:
        return render_template("failure.html")
    new_movie = Movie(title=title,composer=composer)

    try:
        db.session.add(new_movie)
        db.session.commit()
    except:
        return render_template("failure.html")
        # TODO add separate error message for db failure
    return redirect(url_for('index'))

@app.route("/movie/<int:id>")
def movie(id):
    movie = Movie.query.get(id)
    themes = ["test1", "test2", "test3"]
    return render_template("movie.html", movie=movie, themes=themes)

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    Movie.query.filter(Movie.id == id).delete()
    db.session.commit()
    return redirect(url_for('index'))
