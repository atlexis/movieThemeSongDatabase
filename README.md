# Movie Theme Song Database

Movie Theme Song Database is a web service which links movies from imdb together with a list of spotify uris for the most significant soundtracks.

This web service is part of a school project and developed to be used by [flickguess](https://www.github.com/lupont/flickguess).

It uses Python Flask microframework for serving.

## Getting the server to run

### Virtual environment
1. Make sure that Python 3.7+ is installed
2. Navigate to the folder _movieThemeSongDatabase_ using the terminal
3. Type in `$ . venv/bin/activate` to start the virtual environment

### Starting the server
1. Make sure you are in the _movieThemeSongDatabase_ folder and that the virtual environment is started.
2. Type in `$ flask run` to start a local server on address `localhost:5000`

## Versions

### Version 0.1
- Display contents of database at root
- Add content to database using forms and submit button
- Supported content is a movie title and a composer
- Using jinja to extend _layout.html_
- Using jinja to dynamically add content to the html file
