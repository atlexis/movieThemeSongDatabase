from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from mtsdb.auth import login_required
from mtsdb.db import get_db

bp = Blueprint('web', __name__)


@bp.route("/")
def index():
    return redirect(url_for('web.movies'))


@bp.route("/movies")
def movies():
   # get all movies from db
    db = get_db()
    movies = db.execute(
        'SELECT id, title, imdb '
        'FROM movie '
        'ORDER by title'
    ).fetchall()
        
    return render_template("web/index.html", movies=movies) # render html with queried movies


@bp.route("/create", methods=('GET', 'POST'))
@login_required
def create_movie():
    if request.method == 'POST':
        title = request.form['title']
        imdb = request.form['imdb']
        error = None

        if not title:
            error = 'Title is required.'

        if not imdb:
            error = 'IMDB id is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO movie (title, imdb) '
                'VALUES (?, ?)',
                (title, imdb)
            )
            db.commit()
            return redirect(url_for('web.index'))
    return render_template('web/create_movie.html')



@bp.route("/movies/<int:id>")
def movie(id):
    db = get_db()
    movie = db.execute(
        'SELECT * '
        'FROM movie '
        'WHERE id = ?',
        (str(id),)
    ).fetchone()
    if movie is None:
        flash('No movie with id was found')
        redirect(url_for('web.index'))
    
    themes = db.execute(
        'SELECT * '
        'FROM theme '
        'WHERE movie = ?',
        (str(movie['id']),)
        ).fetchall()
    return render_template("web/movie.html", movie=movie, themes=themes)

@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@login_required
def update_movie(id):
    movie = check_movie(id)
    
    if request.method == 'POST':
        title = request.form['title']
        imdb = request.form['imdb']

        if not title or not imdb:
            flash('Please fill in all fields')
        else:
            db = get_db()
            db.execute(
                'UPDATE movie SET title = ?, imdb = ? '
                'WHERE id = ?',
                (title, imdb, str(id))
            )
            db.commit()
            return redirect(url_for('web.movie', id=id))

    return render_template('web/update_movie.html', movie=movie)


@bp.route('/delete/<int:id>', methods=('POST',))
@login_required
def delete_movie(id):
    check_movie(id)
    db = get_db()
    db.execute('DELETE FROM movie WHERE id = ?',
    (id,))
    db.execute('DELETE FROM theme WHERE movie = ?',
    (id,))
    db.commit()

    return redirect(url_for('web.index'))


def check_movie(id):
    movie = get_db().execute(
        'SELECT * '
        'FROM movie '
        'WHERE id = ?',
        (id,)
    ).fetchone()

    if movie is None:
        abort(404, "Movie id {0} doesn't exist.".format(id))

    if g.user is None:
        abort(403)

    return movie


@bp.route('/movies/<int:id>/create', methods=['GET', 'POST'])
@login_required
def create_theme(id):
    db = get_db()
    if request.method == 'POST':
        title = request.form.get('title')
        composer = request.form.get('composer')
        spotify = request.form.get('spotify')

        if not title or not composer or not spotify:
           flash('Please fill in all fields')
        else:
            db.execute(
                'INSERT INTO theme (title, composer, spotify, movie) '
                'VALUES (?, ?, ?, ?)',
                (title, composer, spotify, str(id),)
            )
            db.commit()
            return redirect(url_for('web.movie', id=id))
       
    movie = db.execute(
        'SELECT id, title '
        'FROM movie '
        'WHERE id = ?',
        (str(id),)
    ).fetchone()
    return render_template('web/create_theme.html', movie=movie)


@bp.route("/theme/<int:id>")
def theme(id):
    db = get_db()
    theme = db.execute(
        'SELECT t.id, t.title, composer, spotify, m.id AS mid, m.title AS mtitle, imdb '
        'FROM theme t JOIN movie m ON t.movie = m.id '
        'WHERE t.id = ?',
        (str(id),)
    ).fetchone()
    return render_template("web/theme.html", theme=theme)


@bp.route("/theme/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_theme(id):
    theme = check_theme(id)

    if request.method == 'POST':
        title = request.form['title']
        composer = request.form['composer']
        spotify = request.form['spotify']

        if not title or not composer or not spotify:
            flash('Please fill in all fields')
        else:
            db = get_db()
            db.execute(
                'UPDATE theme SET title = ?, composer = ?, spotify = ? '
                'WHERE id = ?',
                (title, composer, spotify, str(id),)
            )
            db.commit()
            return redirect(url_for('web.theme', id=id))

    return render_template('web/update_theme.html', theme=theme)


@bp.route("/theme/<int:id>/delete", methods=['POST'])
@login_required
def delete_theme(id):
    theme = check_theme(id)
    db = get_db()
    db.execute('DELETE FROM theme WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('web.movie', id=theme['mid']))
    


def check_theme(id):
    theme = get_db().execute(
        'SELECT t.id, t.title, composer, spotify, m.id AS mid, m.title AS mtitle, m.imdb AS imdb '
        'FROM theme t JOIN movie m ON t.movie = m.id '
        'WHERE t.id = ?',
        (str(id),)
    ).fetchone()

    if theme is None:
        abort(404, "Theme id {0} doesn't exist.".format(id))

    if g.user is None:
        abort(403)

    return theme
