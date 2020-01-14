from flask import (Blueprint, redirect, render_template, request, jsonify, abort)

from mtsdb.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api/v1')

# API routes and methods
# The following routes and methods serve as the API endpoints.
# Proper documentation are provided in the '/templates/documentation.html' file

# converts parameter to json and adds a header to avoid cors-problems
def convert(param):
    response = jsonify(param)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# Render the API documentation
@bp.route("/")
def api_documentation():
    return render_template('documentation.html')

def get_themes(id):
    db = get_db()
    themes = []
    theme_query = db.execute(
        'SELECT id, title, composer, spotify '
        'FROM theme WHERE movie = ?',
        (str(id))
    ).fetchall()
    for theme in theme_query:
        themes.append(dict(theme))
    return themes

# create a list of all movies in database, each with a list of it's associated themes,
# and serve as a JSON object
@bp.route("/movies")
def api_get_movies():
    db = get_db()
    movie_query = db.execute(
        'SELECT * '
        'FROM movie '
    ).fetchall()

    movies = []

    for movie in movie_query:
        dict_movie=dict(movie)
        dict_movie['themes'] = get_themes(movie['id'])
        movies.append(dict_movie)
    return convert(movies)

# create an object with specified movie and serve as a JSON object.
@bp.route("/movies/<int:id>", methods=["GET"])
def api_get_movie(id):
    db = get_db()
    movie_query = db.execute(
        'SELECT * '
        'FROM movie '
        'WHERE id = ?',
        (str(id))
    ).fetchone()

    if movie_query is None:
        abort(404, 'No movie with specified id found') # if no movie with id is found, send 404
    movie = dict(movie_query)
    movie['themes'] = get_themes(movie_query['id'])
    return convert(movie)

# create a list of all themes in database, each with some info about it's parent movie,
# and serve as a JSON object.
@bp.route("/themes", methods=["GET"])
def api_get_themes():
    db = get_db()
    theme_query = db.execute(
        'SELECT t.id, t.title, composer, spotify, m.title AS "movie title", imdb AS "movie imdb" '
        'FROM theme t JOIN movie m ON t.movie = m.id '
    ).fetchall()
    themes = []
    for theme in theme_query:
        themes.append(dict(theme))

    return convert(themes)

# create an object with specified theme, with some info about it's parent movie,
# and serve as a JSON object.
@bp.route("/themes/<int:id>")
def api_get_theme(id):
    db = get_db()
    theme = db.execute(
        'SELECT t.id, t.title, composer, spotify, m.title AS "movie title", imdb AS "movie imdb" '
        'FROM theme t JOIN movie m ON t.movie = m.id '
        'WHERE t.id = ?', (str(id))
    ).fetchone()

    if theme is None:
        abort(404, 'No theme with specified id was found')

    return convert(dict(theme))

# create a list, with a certain number of lists in, each with a certain number of theme objects, and serve as JSON object
# needs to arguments to work: questions and options. See documentation for more information.
# this endpoint is implemented with the functionality of Flickguess (github.com/lupont/flickguess) in mind
# this endpoint needs every movie in database to have at least one associated theme with it, otherwise it won't work properly
@bp.route("/themes/random")
def api_get_random():
    questions = request.args.get('questions','') # get param from url
    options = request.args.get('options','') # get param from url
    if not questions or not options: # if no params are specified, return a 400 and simple text error message
        abort(400, 'Provide questions and options query params')
    try:
        if int(questions) < 1 or int(options) < 1:
            abort(400, 'Provide positive integers as parameters')
    except:
        abort(400, 'Provide positive integers as parametrs')

    db = get_db()
    movie_query = db.execute(
        'SELECT id FROM movie '
        'ORDER BY RANDOM() LIMIT ?',
        (questions,)
    ).fetchall()
    movie_ids = []

    for movie in movie_query: # add each movie's id to list
        movie_ids.append(movie['id'])

    if len(movie_ids) < int(questions):
        abort(400, 'Not enough movies in database')

    questions = []
    
    for id in movie_ids:
        question = []
        answer = db.execute(
            'SELECT t.title, composer, spotify, m.title AS "movie title", imdb '
            'FROM theme t JOIN movie m ON t.movie = m.id '
            'WHERE t.movie = ? '
            'ORDER BY RANDOM() LIMIT 1',
            (str(id),)
        ).fetchone()
        question.append(dict(answer))
        movie_query = db.execute(
            'SELECT id FROM movie '
            'WHERE id <> ? '
            'ORDER BY RANDOM() LIMIT ?-1',
            (str(id),options)
        ).fetchall()
        for movie in movie_query:
            alternative = db.execute(
                'SELECT t.title, composer, spotify, m.title AS "movie title", imdb '
                'FROM theme t JOIN movie m ON t.movie = m.id '
                'WHERE t.movie = ? '
                'ORDER BY RANDOM() LIMIT 1',
                (str(movie['id']),)
            ).fetchone()
            question.append(dict(alternative))
        if len(question) < int(options):
            abort(400, 'Not enough movies in database')
        questions.append(question)
    return convert(questions)

# creates a list of a specified number of random themes, but only one from each movie, and serves as JSON
@bp.route("/themes/random/<int:nbr>")
def api_get_random_themes(nbr):

    db = get_db()
    movie_query = db.execute(
        'SELECT id FROM movie '
        'ORDER BY RANDOM() LIMIT ?',
        (str(nbr),)
    ).fetchall()

    if nbr > len(movie_query):
        abort(400, 'Not enough movies in database')

    themes = []
    for movie in movie_query:
        theme = db.execute(
            'SELECT t.title, composer, spotify, m.title as "movie title", imdb AS "movie imdb" '
            'FROM theme t JOIN movie m ON t.movie = m.id '
            'WHERE t.movie = ? '
            'ORDER BY RANDOM() LIMIT 1',
            (str(movie['id']))
        ).fetchone()
        themes.append(dict(theme))

    return (convert(themes))


# create an object based on specified spotify id, serve as a JSON object
@bp.route("/themes/spotify/<id>", methods=["GET"])
def api_get_theme_spotify(id):
    db = get_db()

    theme_query = db.execute(
        'SELECT t.id, t.title, composer, spotify, m.title AS "movie title", imdb AS "movie imdb" '
        'FROM theme t JOIN movie m ON t.movie = m.id '
        'WHERE spotify = ?',
        (id,)
    ).fetchone()

    if theme_query is None:
        abort(404, "Theme with specified id wasn't found")

    return convert(dict(theme_query))
