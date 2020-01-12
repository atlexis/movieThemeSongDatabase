from flask import Flask, render_template, request, redirect, url_for, jsonify, Blueprint, flash, abort
from flask_sqlalchemy import SQLAlchemy
from api.models import Movie, Theme
from . import db
import random

# Author: Alexander Libot

# This module contains routing, HTTP method filtering and API request logic.
# It either serves an HTML template or creates a JSON object.
# First are the routes and methods for the graphical interface
# and later the routes and methods for the API endpoints.

main = Blueprint('main', __name__)

# message to flash after server error
server_error_msg = 'Internal server error, sorry for the inconvenience'

# the following routes and methods are used for the graphical
# root webpage, redirects to /movies
@main.route("/", methods=['GET'])
def index():
    return redirect(url_for('main.movies'))

# home page, list of all movies
@main.route("/movies", methods=["GET"])
def movies():
    movies = Movie.query.order_by(Movie.title).all() # get all movies from db
    return render_template("index.html", movies=movies) # render html with queried movies

# add new movie to database, redirects to /
# flashes a message if something went wrong
@main.route("/add", methods=["POST"])
def add():
    # get data from user
    title = request.form.get("title")
    imdb = request.form.get("imdb")
    if not title or not imdb: # check if data is missing
        flash('Please fill in both fields before submitting')
        return redirect(url_for('main.index'))
    new_movie = Movie(title=title,imdb=imdb) # new database row

    try: # add to database
        db.session.add(new_movie)
        db.session.commit()
    except: # if it can't be added to database
        flash(server_error_msg)
        return redirect(url_for('main.index'))
    flash("Movie '" + title + "' was added") # flash if successful
    return redirect(url_for('main.index')) # redirect to root

# renders the 'templates/movie.html' file
# info about a certain movie object and a list of it's themes
@main.route("/movie/<int:id>")
def movie(id):
    movie = Movie.query.get(id)
    themes = Theme.query.filter_by(movie=id) 
    return render_template("movie.html", movie=movie, themes=themes)

# deletes movie and all associated themes from database, redirects to /
@main.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    moviename = Movie.query.get(id).title # get movie name for message flashing
    try: # deletes from database, flash if successful
        Movie.query.filter(Movie.id == id).delete()
        Theme.query.filter(Theme.movie == id).delete() # delete all themes with movie fk
        db.session.commit()
        flash("Movie '" + moviename + "' was deleted")
    except: # if it can't be deleted from database
        flash(server_error_msg)
    return redirect(url_for('main.index')) # redirect to root

# renders the 'templates/theme.html' file
# info about a certain theme object
@main.route("/theme/<int:id>")
def theme(id):
    theme = Theme.query.get(id)
    return render_template("theme.html", theme=theme)

# add theme to the database, redirects to /movie/id
@main.route("/theme/add/<int:mid>", methods=["POST"])
def add_title(mid):
    title = request.form.get("title")
    composer = request.form.get("composer")
    spotify = request.form.get("spotify")
    if not title or not composer or not spotify: # error check if data is missing
        flash('Please fill in all fields before submitting')
        return redirect(url_for('main.movie',id=mid))
    new_theme = Theme(title=title,composer=composer,spotify=spotify,movie=mid) # new theme object

    try: # add theme to database
        db.session.add(new_theme)
        db.session.commit()
        flash("Theme '" + title + "' was added") # flash success
    except:
        flash(server_error_msg) # flash failure
    return redirect(url_for("main.movie",id=mid)) # redirect to /movie/id

# delete a theme from the database, redirects to /movie/id
@main.route("/theme/delete/<int:id>", methods=["POST"])
def delete_title(id):
    theme = Theme.query.get(id).title # get theme title for message flashing
    try: # delete theme from database
        mid = Theme.query.get(id).movie # get movie id for redirect
        Theme.query.filter(Theme.id == id).delete()
        db.session.commit()
        flash("Theme '" + theme + "' was deleted") # flash success
    except:
        flash(server_error_msg) # flash failure
    return redirect(url_for("main.movie",id=mid)) # redirect to /movie/id

# API routes and methods
# The following routes and methods serve as the API endpoints.
# Proper documentation are provided in the '/templates/documentation.html' file

# converts parameter to json and adds a header to avoid cors-problems
def convert(param):
    response = jsonify(param)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# Render the API documentation
@main.route("/api/v1", methods=["GET"])
def api_documentation():
    return render_template('documentation.html')

# create a list of all movies in database, each with a list of it's associated themes,
# and serve as a JSON object
@main.route("/api/v1/movies", methods=["GET"])
def api_get_movies():
    movie_list = Movie.query.all() # get all movie rows from db
    movies = [] # create list to return

    for movie in movie_list: # add data from every movie to list
        themes = []
        theme_list = Theme.query.filter_by(movie=movie.id) # get all associated themes
        for theme in theme_list: # add data from every theme to associated movie
            themes.append({'title' : theme.title, 'composer' : theme.composer, 'spotify' : theme.spotify})
        movies.append({'id' : movie.id, 'title' : movie.title, 'imdb' : movie.imdb, 'themes' : themes})
            
    return convert(movies)

# create an object with specified movie and serve as a JSON object.
@main.route("/api/v1/movies/<int:id>", methods=["GET"])
def api_get_movie(id):
    movie_query = Movie.query.get(id) # get movie row from db
    if movie_query is None:
        abort(404) # if no movie with id is found, send 404
    themes = []
    theme_list = Theme.query.filter(Theme.movie==id) # get all associated themes
    for theme in theme_list: # data from every theme to movie
        themes.append({'title' : theme.title, 'composer' : theme.composer, 'spotify' : theme.spotify})
    movie = {'id' : movie_query.id, 'title' : movie_query.title, 'imdb' : movie_query.imdb, 'themes' : themes}
    return convert(movie)

# create a list of all themes in database, each with some info about it's parent movie,
# and serve as a JSON object.
@main.route("/api/v1/themes", methods=["GET"])
def api_get_themes():
    theme_list = Theme.query.all() # get all theme rows
    themes = []

    for theme in theme_list:
        movie = Movie.query.get(theme.movie) # get data from db for associated movie
        themes.append({'id' : theme.id, 'title' : theme.title, 'composer' : theme.composer, 'spotify' : theme.spotify, 'movie title' : movie.title, 'movie imdb' : movie.imdb})
    return convert(themes)

# create an object with specified theme, with some info about it's parent movie,
# and serve as a JSON object.
@main.route("/api/v1/themes/<int:id>", methods=["GET"])
def api_get_theme(id):
    theme_query = Theme.query.get(id) # get theme row from db
    if theme_query is None:
        abort(404) # if no theme with id is found, send 404
    movie = Movie.query.get(theme_query.movie) # get data from db for associated movie
    theme = {'id' : theme_query.id, 'title' : theme_query.title, 'spotify' : theme_query.spotify, 'movie title' : movie.title, 'composer' : theme_query.composer, 'movie imdb' : movie.imdb}
    return convert(theme)

# create a list, with a certain number of lists in, each with a certain number of theme objects, and serve as JSON object
# needs to arguments to work: questions and options. See documentation for more information.
# this endpoint is implemented with the functionality of Flickguess (github.com/lupont/flickguess) in mind
# this endpoint needs every movie in database to have at least one associated theme with it, otherwise it won't work properly
@main.route("/api/v1/themes/random", methods=["GET"])
def api_get_random():
    questions = request.args.get('questions','') # get param from url
    options = request.args.get('options','') # get param from url
    if not questions or not options: # if no params are specified, return a 400 and simple text error message
        return 'Provide questions and options query params', 400
    movie_query = Movie.query.all() # get all movie rows from db
    movies = []

    for movie in movie_query: # add each movie's id to list
        movies.append({'id' : movie.id})
        
    # get a specified number of random movie ids
    random.shuffle(movies)
    movies = movies[:int(questions)]

    mlist = [] # used for storing the structure of the JSON response, but with an id instead of theme objects

    # get a list of lists, where every first element in the inner lists are unique from the other first elements
    # and each element in the inner lists are unique from each other and in random order
    for movie in movies:
        other = []
        for movie2 in movie_query:
            if movie['id'] != movie2.id:
                other.append({'id': movie2.id})
        random.shuffle(other)
        other = other[:int(options)-1]
        other.insert(0,{'id': movie['id']})
        mlist.append(other)

    movies = [] # used for storing the list to be returned

    # keeps the structure of the mlist list.
    # gets a random theme from each element in mlist and adds it to a new list with the same structure.
    # also gets data about each theme's associated movie.
    for i in range(0,len(mlist)): # keep the structure of mlist
        level = []
        for j in range(0,len(mlist[i])): # keep the structure of mlist
            movie = Movie.query.get(mlist[i][j]) # get movie row based on id in mlist
            theme_query = Theme.query.filter_by(movie=mlist[i][j]['id']) # get associated themes
            themes = []
            for theme in theme_query: # add data from themes
                themes.append({'id': theme.id, 'title': theme.title, 'composer': theme.composer, 'spotify': theme.spotify})
            # get a random theme and add it to a list along with info about associated movie
            random.shuffle(themes)
            if len(themes) > 0:
                theme = themes[0]
                level.append({'title': theme['title'], 'composer': theme['composer'], 'movie title': movie.title, 'imdb': movie.imdb, 'spotify': theme['spotify']})
        movies.append(level) # add each list to this outer list
    return convert(movies)

# creates a list of a specified number of random themes, but only one from each movie, and serves as JSON
@main.route("/api/v1/themes/random/<int:nbr>", methods=["GET"])
def api_get_random_themes(nbr):
    movie_list = Movie.query.all() # get all movies
    movies = []

    # get all themes for all movies
    for movie in movie_list:
        themes = []
        theme_list = Theme.query.filter_by(movie=movie.id)
        for theme in theme_list:
            themes.append({'title' : theme.title, 'composer' : theme.composer, 'spotify' : theme.spotify})
        if len(themes) > 0:
            movies.append({'id' : movie.id, 'title' : movie.title, 'imdb' : movie.imdb, 'themes' : themes})
    if nbr > len(movies):
        return 'Not enough movies', 400

    # get the specified number of random movies
    random.shuffle(movies)
    movies = movies[:nbr]
    
    # get a random theme from each movie and create a theme object with data from associated movie.
    themes = []
    for movie in movies:
        theme_list = movie['themes']
        random.shuffle(theme_list)
        themes.append({'title' : theme_list[0]['title'], 'composer' : theme_list[0]['composer'], 'spotify' : theme_list[0]['spotify'], 'movie title' : movie['title'], 'movie imdb' : movie['imdb']})
    
    return convert(themes)


# create an object based on specified spotify id, serve as a JSON object
@main.route("/api/v1/themes/spotify/<string:id>", methods=["GET"])
def api_get_theme_spotify(id):
    theme_query = Theme.query.all() # get all theme rows

    for t in theme_query: # if a row with matching spotify id is found, return theme object
        if t.spotify == id:
            movie = Movie.query.get(t.movie)
            theme = {'id' : t.id, 'title' : t.title, 'composer' : t.composer, 'spotify' : t.spotify, 'movie title' : movie.title, 'movie imdb' : movie.imdb}
            return convert(theme)
    return 'Theme with id ' + id + ' not found.', 404 # if no row is found with specified spotify id
