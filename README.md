# Movie Theme Song Database

Movie Theme Song Database is a web service which links movies from imdb together with a list of spotify ids for the most significant soundtracks.

This web service is part of a school project and developed to be used by [flickguess](https://www.github.com/lupont/flickguess).

Uses Python Flask micro framework for serving and SQLite for database.

**Navigation**
- [Getting the server to run](#install)
- [Access](#access)
- [Graphical interface](#gi)
- [API endpoints](#api)
- [Code example](#code)
- [Versions](#versions)

## <a name='install'></a> Getting the server to run

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

### Setting environment variable
1. Make sure you are in the _movieThemeSongDatabase_ folder and that the virtual environment is started.
2. Set the environment variable by typing `$ export FLASK_APP=api`

### Starting the server
1. Make sure you are in the _movieThemeSongDatabase_ folder, that the virtual environment is started and that all dependencies are installed
2. Type in `$ flask run` to start a local server on address `localhost:5000`

## <a name='access'></a> Access
There are two ways to access the data in the database; the first way is through the [graphical interface](#gi) and the second way is by using the [API endpoints](#api).

## <a name='gi'></a> Graphical interface
The web service is not yet deployed so when the application is run on your own machine the base url is [localhost:5000/](http://localhost:5000/) (or another specified port).

The graphical interface is the only way to add or delete data from the database, but you can access the data with the [API endpoints](#api) as well. The data can be accessed, deleted and created without any authentication.

### Movies
The main page is at `/movies` and contains a list of movies which can be clicked. At the top of the page is a form which can be filled in to add a new movie to the database. Each movie needs to be associated with an IMDB id, which can be seen in the URL of movies on the [IMDB website](https://www.imdb.com). E.g. [www.imdb.com/title/tt0120737/](https://www.imdb.com/title/tt0120737/) where **tt0120737** is the id.
  
### <a name='themes'> Themes
Each movie has it's own page **/movies/_id_** (id is this web service's own id)  where _id_, _title_, _IMDB id_ and a list of theme songs can be viewed. The movie can be deleted with the button at the bottom of the page. Deleting a movie will also delete all of it's associated theme songs. A new theme song can be added by filling out the form at the bottom of the theme songs list. Each theme song needs a title, composer and a spotify id. The spotify id is used in spotify URIs to identify a specific song. E.g. [https://open.spotify.com/track/3ZSf1TJZyRb0rnWYuUtdX4](https://open.spotify.com/track/3ZSf1TJZyRb0rnWYuUtdX4) where **3ZSf1TJZyRb0rnWYuUtdX4** is the id.

An individual theme can be accessed by clicking on it. It has the url **/theme/_id_**. A theme page contains _id_, _title_ and _spotify id_. A theme can be deleted by pressing the button at the bottom of the page.

### Note
- The id for accessing movies and themes is only used for navigation and access on the website and has no other use.
- Movies or themes can't be added through a url but must be added through the forms.
- Movies or themes can be deleted through a POST request to **/delete/_id_** or **/theme/delete/_id_**, but is preferably deleted through the graphical interface (or not at all).

## <a name='api'> API endpoints
This application provides a number of different endpoint for accessing the data in the database in different ways. The data can only be read, not created, updated or deleted through the api calls. If you wish to add or delete data, see the [Graphical interface](#gi) section. All data are recieved as JSON files.

Whenever _id_ or any other part of the url is written in cursive, it should be substituted for a positive integer. See each specific endpoint for more information.

The base adress for api calls are `/api/v1`

### Movies
#### GET /movies
Get a list of all movies in the database. The list contains id, title, imdb id and an array of themes containing: title, composer and spotify id.

##### Input
None

##### Return data
```json
[
  {
    "id": 1,
    "imdb": "tt0076759",
    "themes": [
      {
        "composer": "John Williams",
        "spotify": "3ZSf1TJZyRb0rnWYuUtdX4",
        "title": "Main Title"
      },
      {
        "composer": "John Williams",
        "spotify": "5ZSAdkQb23NPIcUGt6exdm",
        "title": "Cantina Band"
      }
    ],
    "title": "Star Wars"
  },
  {
    "id": 2,
    "imdb": "tt0073195",
    "themes": [
      {
        "composer": "John Williams",
        "spotify": "55xly70WJY1cx5qsoogaqs",
        "title": "Main Title"
      }
    ],
    "title": "Jaws"
  },
  ...
]
```

#### GET /movies/_id_
Get information about a certain movie. The id in the url is determining what movie is recieved.

##### Input
None

##### Return data
Returns a 404 if a movie with specified id isn't found, otherwise:
```json
{
  "id": 3,
  "imdb": "tt0120737",
  "themes": [
    {
      "composer": "Howard Shore",
      "spotify": "644es5aYPJghtZLjM1rmSP",
      "title": "Concerning Hobbits"
    },
    {
      "composer": "Howard Shore",
      "spotify": "6HYCOHzY2xR4W2dOokH3ed",
      "title": "The Bridge of Khazad Dum"
    }
  ],
  "title": "The Lord of the Rings: The Fellowship of the Ring"
}
```

### Themes
#### GET /themes
Get a list of all themes in the database. The list contains id, title, composer, movie title, imdb id and spotify id.

##### Input
None

##### Return data
```json
[
  {
    "composer": "John Williams",
    "id": 1,
    "movie imdb": "tt0076759",
    "movie title": "Star Wars",
    "spotify": "3ZSf1TJZyRb0rnWYuUtdX4",
    "title": "Main Title"
  },
  {
    "composer": "John Williams",
    "id": 2,
    "movie imdb": "tt0076759",
    "movie title": "Star Wars",
    "spotify": "5ZSAdkQb23NPIcUGt6exdm",
    "title": "Cantina Band"
  },
  ...
]
```

#### GET /themes/_id_
Get a information about a certain theme. The id in the url is determining what theme. is recieved.

##### Input
None

##### Return data
Returns a 404 if a theme with specified id isn't found, otherwise:
```json
{
  "composer": "Howard Shore",
  "id": 18,
  "movie imdb": "tt0903624",
  "movie title": "The Hobbit: An Unexpected Journey",
  "spotify": "1yJzoX4xPsACzVxUarXRKa",
  "title": "Misty Mountains"
}
```

#### GET /themes/random/_nbr_
Get a list of random theme(s) from the database, with only one theme from each movie and each theme is guaranteed to be unique. Specify how many with _nbr_. Should be a positive integer, otherwise returns an 404. If _nbr_ is larger than the number of movies in the database, a 400 is returned.

##### Input
None

##### Return data
The example is for a call to /themes/random/3
```json
[
  {
    "composer": "Ray Parker, Jr.",
    "movie imdb": "tt0087332",
    "movie title": "Ghostbusters",
    "spotify": "3m0y8qLoznUYi73SUBP8GI",
    "title": "Ghostbusters"
  },
  {
    "composer": "John Williams",
    "movie imdb": "tt0078346",
    "movie title": "Superman",
    "spotify": "5My95PvNVMMSkgcxv75lvE",
    "title": "Main Title"
  },
  {
    "composer": "Terry Gilkyson",
    "movie imdb": "tt0061852",
    "movie title": "The Jungle Book",
    "spotify": "7EA9SlGReyET1cYHIeFbIH",
    "title": "The Bare Necessities"
  }
]
```

#### GET /themes/spotify/_id_
Get information about a certain theme. The id in the url is a spotify id, see [here](#themes) what the id is.

##### Input
None

##### Return data
Returns a 404 if a theme with specified id isn't found. The example is for a call to /themes/spotify/55xly70WJY1cx5qsoogaqs

```json
{
  "composer": "John Williams",
  "id": 3,
  "movie imdb": "tt0073195",
  "movie title": "Jaws",
  "spotify": "55xly70WJY1cx5qsoogaqs",
  "title": "Main Title"
}
```

#### <a name='random'> GET /themes/random?questions=_nbr_&options=_nbr_ 
Get a list with a number of lists containing a number of random themes. Uses two query parameters for determining the size of the outer list and the size of all the inner lists.

##### Input
The _questions_ parameter determines the size of the outer list, i.e. how many lists it contains.

The _options_ parameter detemines the size of the inner lists, i.e. how many themes they each contain.

##### Return data
The example is for a call to /themes/random?questions=2&options=3
```json
[
  [
    {
      "composer": "Lin-Manuel Miranda",
      "imdb": "tt3521164",
      "movie title": "Moana",
      "spotify": "3KzemxaWSSiYtnzOokd0Rs",
      "title": "How Far I'll Go"
    },
    {
      "composer": "Alan Menken",
      "imdb": "tt0119282",
      "movie title": "Hercules",
      "spotify": "0D1OY0M5A0qD5HGBvFmFid",
      "title": "Go the Distance"
    },
    {
      "composer": "Ray Parker, Jr.",
      "imdb": "tt0087332",
      "movie title": "Ghostbusters",
      "spotify": "3m0y8qLoznUYi73SUBP8GI",
      "title": "Ghostbusters"
    }
  ],
  [
    {
      "composer": "John Williams",
      "imdb": "tt0082971",
      "movie title": "Raiders of the Lost Ark",
      "spotify": "1YYKKW40noxJ8BNBODnriF",
      "title": "Raiders March"
    },
    {
      "composer": "Terry Gilkyson",
      "imdb": "tt0061852",
      "movie title": "The Jungle Book",
      "spotify": "7EA9SlGReyET1cYHIeFbIH",
      "title": "The Bare Necessities"
    },
    {
      "composer": "Dolly Parton",
      "imdb": "tt0103855",
      "movie title": "The Bodyguard",
      "spotify": "4eHbdreAnSOrDDsFfc4Fpm",
      "title": "I Will Always Love You"
    }
  ]
]
```

## <a name='code'></a> Code example
The following example uses one of the APIs endpoints; [GET /themes/random](#random). It is written in JavaScript in the React framework, but any language which can handle API calls and JSON objects can use the API in a similar way.

The method in this example fetches a two-dimensional array of random theme objects from the web service, it stores some data from the first element of each inner array as answer and some other data from all the elements of each inner array as options, then shuffles the options and stores both variables in a global array. This is reapeated for each inner array.

First the API must be called which is done here on line 2 with the fetch function. This endpoint needs two query parameters in the URL. The response is stored in a variable. The API response is a JSON file, but it has to be 'converted' for Javascript to know that it should interpret it as such - line 3.

Since the JSON response consist of a nested list/array, the elements (theme objects) can be accessed as a normal JavaScript two-dimensional array, by specifying the wanted indexes – line 8. The parameters of a theme object can be accessed as a normal JavaScript object - lines 11-15.

Theme object parameters can also be accessed directly from the JSON file – lines 20-21.

```javascript
1  async fetchQuizData(nbrOfQuestions, nbrOfOptions) {
2    const response = await fetch(`http://localhost:5000/api/v1/themes/random
       ?questions=${nbrOfQuestions}&options=${nbrOfOptions}`);
3    const json = await response.json();
4
5    let answer = '';
6    for (let i = 0; i < json.length; i++) {
7      const options = [];
8      const current = json[i][0];
9
10     answer = {
11       title: current['movie title'],
12       spotify: current['spotify'],
13       song: current['title'],
14       composer: current['composer'],
15       correct: false,
16     };
17
18     for (let j = 0; j < json[i].length; j++) {
19       options.push({
20         'movie title': json[i][j]['movie title'],
21         imdb: json[i][j]['imdb'],
22       });
23     }
24
25     shuffle(options);
26     addToQuizData(options, answer);
27   }
28
29   this.setState({ spotifyId: quizData[0].answer.spotify });
30   await this.fetchMoviePosters();
31   this.setState({ isLoading: false });
32 }
```

## <a name='versions'></a> Versions

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

#### Version 0.6.3
- Added more data to the database

### Version 0.7 - Documentation, documentation, documentation
- Added an API documentation page
- Updated documentation in readme with better API endpoints explanation, and a code example
- Added documentation in the code
