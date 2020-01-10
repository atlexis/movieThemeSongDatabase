from flask import Flask, render_template, request, redirect, url_for, jsonify, Blueprint, flash
from flask_sqlalchemy import SQLAlchemy
from api.models import Movie, Theme
from . import db
import random

main = Blueprint('main', __name__)

server_error_msg = 'Internal server error, sorry for the inconvenience'

# root webpage, redirects to /movies
@main.route("/", methods=['GET'])
def index():
    return redirect(url_for('main.movies'))

# home page, list of all movies
@main.route("/movies", methods=["GET"])
def movies():
    movies = Movie.query.order_by(Movie.title).all()
    return render_template("index.html", movies=movies)

# add data to database, redirects to /movies or shows error page
@main.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    imdb = request.form.get("imdb")
    if not title or not imdb: # error check
        flash('Please fill in both fields before submitting')
        return redirect(url_for('main.index'))
    new_movie = Movie(title=title,imdb=imdb)

    try:
        db.session.add(new_movie)
        db.session.commit()
    except:
        flash(server_error_msg)
        return redirect(url_for('main.index'))
    flash("Movie '" + title + "' was added")
    return redirect(url_for('main.index'))

@main.route("/movie/<int:id>")
def movie(id):
    movie = Movie.query.get(id)
    themes = Theme.query.filter_by(movie=id)
    return render_template("movie.html", movie=movie, themes=themes)

@main.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    moviename = Movie.query.get(id).title
    try:
        Movie.query.filter(Movie.id == id).delete()
        Theme.query.filter(Theme.movie == id).delete()
        db.session.commit()
    except:
        flash(server_error_msg )
    flash("Movie '" + moviename + "' was deleted")
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
        flash('Please fill in all fields before submitting')
        return redirect(url_for('main.movie',id=mid))
    new_theme = Theme(title=title,composer=composer,spotify=spotify,movie=mid)

    try:
        db.session.add(new_theme)
        db.session.commit()
    except:
        flash(server_error_msg)
        return redirect(url_for('main.movie',id=mid))
    flash("Theme '" + title + "' was added")
    return redirect(url_for("main.movie",id=mid))

@main.route("/theme/delete/<int:id>", methods=["POST"])
def delete_title(id):
    theme = Theme.query.get(id).title
    try:
        mid = Theme.query.get(id).movie
        Theme.query.filter(Theme.id == id).delete()
        db.session.commit()
    except:
        flash(server_error_msg)
    flash("Theme '" + theme + "' was deleted")
    return redirect(url_for("main.movie",id=mid))

@main.route("/api/v1/movies", methods=["GET"])
def api_get_movies():
    movie_list = Movie.query.all()
    movies = []

    for movie in movie_list:
        themes = []
        theme_list = Theme.query.filter_by(movie=movie.id)
        for theme in theme_list:
            themes.append({'title' : theme.title, 'composer' : theme.composer, 'spotify' : theme.spotify})
        movies.append({'id' : movie.id, 'title' : movie.title, 'imdb' : movie.imdb, 'themes' : themes})
            
    return jsonify(movies)

@main.route("/api/v1/movies/<int:id>", methods=["GET"])
def api_get_movie(id):
    movie_query = Movie.query.get(id)
    themes = []
    theme_list = Theme.query.filter(Theme.movie==id)
    for theme in theme_list:
        themes.append({'title' : theme.title, 'composer' : theme.composer, 'spotify' : theme.spotify})
    movie = {'id' : movie_query.id, 'title' : movie_query.title, 'imdb' : movie_query.imdb, 'themes' : themes}
    return jsonify(movie)

@main.route("/api/v1/themes", methods=["GET"])
def api_get_themes():
    theme_list = Theme.query.all()
    themes = []

    for theme in theme_list:
        movie = Movie.query.get(theme.movie)
        themes.append({'id' : theme.id, 'title' : theme.title, 'composer' : theme.composer, 'spotify' : theme.spotify, 'movie title' : movie.title, 'movie imdb' : movie.imdb})
    return jsonify(themes)

@main.route("/api/v1/themes/<int:id>", methods=["GET"])
def api_get_theme(id):
    theme_query = Theme.query.get(id)
    movie = Movie.query.get(theme_query.movie)
    theme = {'id' : theme_query.id, 'title' : theme_query.title, 'spotify' : theme_query.spotify, 'movie title' : movie.title, 'composer' : theme_query.composer, 'movie imdb' : movie.imdb}
    return jsonify({"themes" : theme})

@main.route("/api/v1/themes/random", methods=["GET"])
def api_get_random_theme():
    theme_list = Theme.query.all() 
    themes = []

    for theme in theme_list:
        movie = Movie.query.get(theme.movie)
        themes.append({'id' : theme.id, 'title' : theme.title, 'composer' : theme.composer, 'spotify' : theme.spotify, 'movie title' : movie.title, 'movie imdb' : movie.imdb})
    rint = random.randint(0,len(themes)-1)

    return jsonify(themes[rint])

@main.route("/api/v1/themes/random/<int:nbr>", methods=["GET"])
def api_get_random_themes(nbr):
    if nbr == 1:
        return api_get_random_theme()
    movie_list = Movie.query.all()
    movies = []

    for movie in movie_list:
        themes = []
        theme_list = Theme.query.filter_by(movie=movie.id)
        for theme in theme_list:
            themes.append({'title' : theme.title, 'composer' : theme.composer, 'spotify' : theme.spotify})
        if len(themes) > 0:
            movies.append({'id' : movie.id, 'title' : movie.title, 'imdb' : movie.imdb, 'themes' : themes})
    if nbr > len(movies):
        return 'Not enough movies', 400

    random.shuffle(movies)
    movies = movies[:nbr]
    themes = []
    for movie in movies:
        theme_list = movie['themes']
        random.shuffle(theme_list)
        themes.append({'title' : theme_list[0]['title'], 'composer' : theme_list[0]['composer'], 'spotify' : theme_list[0]['spotify'], 'movie title' : movie['title'], 'movie imdb' : movie['imdb']})
    
    return jsonify(themes)

@main.route("/api/v1/themes/spotify/<string:id>", methods=["GET"])
def api_get_theme_spotify(id):
    theme_list = Theme.query.all()

    for t in theme_list:
        if t.spotify == id:
            movie = Movie.query.get(t.movie)
            theme = {'id' : t.id, 'title' : t.title, 'composer' : t.composer, 'spotify' : t.spotify, 'movie title' : movie.title, 'movie imdb' : movie.imdb}
            return jsonify(theme)
    return 'Theme with id ' + id + ' not found.', 404
