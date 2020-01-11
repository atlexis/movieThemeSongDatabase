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

### Installing dependencies
1. Make sure you are in the _movieThemeSongDatabase_ folder and that the virtual environment is started.
2. Type in `$ pip install -r requirement.txt`
3. Wait for all dependencies to be installed

### Starting the server
1. Make sure you are in the _movieThemeSongDatabase_ folder, that the virtual environment is started and that all dependencies are installed
2. Type in `$ flask run` to start a local server on address `localhost:5000`

## API

### Movies

- Send a GET request to `/movies` to recieve a JSON object with an array of all movies in database
  - Each movie has fields with: id, title, imdb id and an array with themes containing: title, composer and spotify id

- Send a GET request to `/movies/<id>` to recieve a JSON object of a specific movie in database
  - The movie has fields with: id, title, imdb id and an array with themes containing: title, composer and spotify id
  - Returns code 500 atm if no movie is found with id

### Themes

- Send a GET request to `/themes` to recieve a JSON object with an array of all themes in database
  - Each theme has fields with: id, title, composer, movie title, imdb id and spotify id
  
- Send a GET request to `/themes/<id>` to recieve a JSON object of a specific theme in database
  - The theme has fields with: id, title, composer, movie title, imdb id and spotify id
  - Returns code 500 atm if no theme is found with id

- Send a GET request to `/themes/random/<nbr>` to recieve a JSON object with <nbr> amount of random themes from unique movie, e.g. two themes won't be from the same movie.
  - If <nbr> is larger than the number of movies in the database, a 400 error code will be sent
  - The theme has fields: id, title, composer, movie title, imdb id and spotify id

- Send a GET request to `/themes/spotify/<id>` to recieve a JSON object with the theme with the specified spotify id <id>, if existing, otherwise sends a 404 error.
  - The theme has fields: id, title, composer, movie title, imdb id, spotify id 

- Send a GET request to `/themes/spotify/random?questions=<qnbr>&options=<onbr>` to recive a JSON object with <qnbr> arrays (question array) containing <onbr> arrays (option array) containing theme objects.
  - Every first object in the option array is unique compared to the first element in the other option arrays.
  - Every theme object in a option array are from different movies
  - A theme object contains: id, title, composer, movie title, imdb id, spotify id

## Versions

### Version 0.1 - Getting it out there
- Display contents of database at root
- Add content to database using forms and submit button
- Supported content is a movie title and a composer
- Using jinja to extend _layout.html_
- Using jinja to dynamically add content to the html file

### Version 0.2 - Movie time
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

### Version 0.3 - Pick a theme 
- Added links for all theme songs from a movie
- Added dynamically created theme song page
- Ability to remove theme songs
- Removes all theme songs associated with a movie when movie is deleted

### Version 0.4 - Make an API
- Added api (v1) for getting data
- Ability to get list of movies or a specific movie as JSON object
- Ability to get list of themes or a specific theme as JSON object

### Version 0.5 - Moving around
- Changed structure to make it easier to remake database
- Changed the composer attribute from Movie entity to Theme entity

#### Version 0.5.1
- Removed old files from before restructure

#### Version 0.5.2
- Changed from serving html failure pages to instead use message flashing
- Small cleanup in the code

### Version 0.6 - No end (point) in sight
- Added new end points; getting a random theme, getting theme object from spotify id
- Added end point for getting a specified number of random theme objects from different movies

#### Version 0.6.1
- Added new end point for getting an array of arrays with random themes, for use by Flickguess
- Removed old `/api/v1/themes/random` endpoint, same functionality can be achieved by the `/api/v1/themes/random/1` endpoint

#### Version 0.6.2
- Resolved issue with calling a removed function for getting a single random theme object
