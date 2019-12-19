# Movie Theme Song Database

Movie Theme Song Database is a web service which links movies from imdb together with a list of spotify ids for the most significant soundtracks.

This web service is part of a school project and developed to be used by [flickguess](https://www.github.com/lupont/flickguess).

Uses Python Flask micro framework for serving and SQLite for database.

## Getting the server to run

### Virtual environment
1. Make sure that Python 3.7+ is installed
2. Make sure that Pip 19.3+ is installed
3. Navigate to the folder _movieThemeSongDatabase_ using the terminal
4. Type in `$ . venv/bin/activate` to start the virtual environment
5. (venv) should appear before the prompt

###Installing dependencies
1. Make sure you are in the _movieThemeSongDatabase_ folder and that the virtual environment is started.
2. Type in `$ pip install -r requirement.txt`
3. Wait for all dependencies to be installed

### Starting the server
1. Make sure you are in the _movieThemeSongDatabase_ folder, that the virtual environment is started and that all dependencies are installed
2. Type in `$ flask run` to start a local server on address `localhost:5000`

## Versions

### Version 0.1
- Display contents of database at root
- Add content to database using forms and submit button
- Supported content is a movie title and a composer
- Using jinja to extend _layout.html_
- Using jinja to dynamically add content to the html file

### Version 0.2
- Added links to all movies at root
- Added dynamically created movie page, with info about movie
- Changed database to include imdb id for movies
- Added theme table to database for theme song, with spotify id
- Ability to add theme songs for movie
- Ability to remove movie from database
- Ability to add a movie with imdb id

#### Version 0.2.1
- Added _requirement.txt_ file for dependencies
- Updated broken installation guide to use _requirement.txt_ file
