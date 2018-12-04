# Inspyre

Team RedSky -- Puneet Johal, Daniel Keriazis, Mai Rachlevsky

## Inspyre Inspires

Users are inspired with content such as poems, vocabulary words, and recommendations for books, movies, and music. Users are able to favorite content that they like for future reference and set a "Goal of the Day" to keep on track and stay motivated.

# To run our project:
1. Clone our repo
```
$ git clone git@github.com:MaiRachlevsky/Inspyre.git
```
2. Create & activate your virtual environment
```
$ python3 -m venv venv
$ . venv/bin/activate
```
3. In your virtual environment, run the following to install the necessary packages:
```
(venv) $ pip install -r <path-to-file>requirements.txt
```
4. Go to the project directory
```
(venv) $ cd Inspyre
```
5. Run app.py
```
(venv) $ python3 app.py 
```
6. Navigate to `localhost:5000` on your web browser


# APIs used in project:
1. Oxford API
We use the Oxford API to generate the word of the day and its definition which we display on the home page. To get a key...
2. Bing API
We use the Bing API to get pcitures which we use for our background. To get a key..
3. Poem API
We use the Poem API to generate a random poem on the user's page in order to inspire them. No key is necessary, location is at [here](https://poemist.github.io/poemist-apidoc/#misc-services)
4. TasteDive API
We use the TasteDive API to provide reccomendations for books, movies, and music.
