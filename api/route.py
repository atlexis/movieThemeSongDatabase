from flask import Flask, render_template, request, redirect, url_for, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy

#configure app
#app = Flask(__name__)

#configure database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
#db = SQLAlchemy(app)

# Import Movie data model, must be imported after db is set to prevent cyclic import conflict
from api.models import Movie, Theme
from . import db

# Run server in debug mode (update when changes are made)
#app.run(debug=True)

main = Blueprint('main', __name__)

# root webpage
@main.route("/", methods=['GET'])
def index():
    return redirect(url_for('main.movies'))

@main.route("/movies", methods=["GET"])
def movies():
    movies = Movie.query.order_by(Movie.title).all()
    return render_template("index.html", movies=movies)
    return 'test'


# just used for post, adds data to database
@main.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    imdb = request.form.get("imdb")
    if not title or not imdb:
        return render_template("failure.html")
    new_movie = Movie(title=title,imdb=imdb)

    try:
        db.session.add(new_movie)
        db.session.commit()
    except:
        return render_template("failure.html")
        # TODO add separate error message for db failure
    return redirect(url_for('main.index'))

@main.route("/movie/<int:id>")
def movie(id):
    movie = Movie.query.get(id)
    themes = Theme.query.filter_by(movie=id)
    return render_template("movie.html", movie=movie, themes=themes)

@main.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    Movie.query.filter(Movie.id == id).delete()
    Theme.query.filter(Theme.movie == id).delete()
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route("/theme/<int:id>")
def theme(id):
    theme = Theme.query.get(id)
    return render_template("theme.html", theme=theme)

@main.route("/theme/add/<int:mid>", methods=["POST"])
def add_title(mid):
    title = request.form.get("title")
    composer = request.form.get("composer")
    spotify = request.form.get("spotify")
    if not title or not composer or not spotify:
        return render_template("failure.html")
    new_theme = Theme(title=title,composer=composer,spotify=spotify,movie=mid)

    try:
        db.session.add(new_theme)
        db.session.commit()
    except:
        return render_template("failure.html")
    return redirect(url_for("main.movie",id=mid))

@main.route("/theme/delete/<int:id>", methods=["POST"])
def delete_title(id):
    mid = Theme.query.get(id).movie
    Theme.query.filter(Theme.id == id).delete()
    db.session.commit()
    return redirect(url_for("main.movie",id=mid))

@main.route("/api/v1/movies", methods=["GET"])
def api_get_movies():
    movie_list = Movie.query.all()
    movies = []

    for movie in movie_list:
        themes = []
        theme_list = Theme.query.filter_by(movie=movie.id)
        for theme in theme_list:
            themes.append({'title' : theme.title, 'spotify' : theme.spotify})
        movies.append({'id' : movie.id, 'composer' : movie.composer, 'title' : movie.title, 'imdb' : movie.imdb, 'themes' : themes})
            
    return jsonify({"movies" : movies})

@main.route("/api/v1/movies/<int:id>", methods=["GET"])
def api_get_movie(id):
    movie_query = Movie.query.get(id)
    themes = []
    theme_list = Theme.query.filter(Theme.movie==id)
    for theme in theme_list:
        themes.append({'title' : theme.title, 'spotify' : theme.spotify})
    movie = {'id' : movie_query.id, 'title' : movie_query.title, 'composer' : movie_query.composer, 'imdb' : movie_query.imdb, 'themes' : themes}
    return jsonify({"movies" : movie})

@main.route("/api/v1/themes", methods=["GET"])
def api_get_themes():
    theme_list = Theme.query.all()
    themes = []

    for theme in theme_list:
        movie = Movie.query.get(theme.movie)
        themes.append({'id' : theme.id, 'title' : theme.title, 'spotify' : theme.spotify, 'movie title' : movie.title, 'composer' : movie.composer})
    return jsonify({"themes" : themes})

@main.route("/api/v1/themes/<int:id>", methods=["GET"])
def api_get_theme(id):
    theme_query = Theme.query.get(id)
    movie = Movie.query.get(theme_query.movie)
    theme = {'id' : theme_query.id, 'title' : theme_query.title, 'spotify' : theme_query.spotify, 'movie title' : movie.title, 'composer' : movie.composer}
    return jsonify({"themes" : theme})

