# What is this?
A visualization of hate crime in Berlin, starting 2005.
The data is kindly provided by [ReachOut - Opferberatung und Bildung gegen Rechtsextremismus, Rassismus und Antisemitismus](http://www.reachoutberlin.de).
It is scraped regularly from their webpage and visualized and analyzed by software written by [Arne Schlüter](https://github.com/aesthaddicts) and [Joshua Widmann](https://github.com/jshwdmnn).

You can see a live demo here: [LiveDemo](http://arne.schlueter.is/working-on/berliner-winter/)

# Documentation
## User group
We target mostly all kinds of politically interested people. We also wanted to raise awareness of the amount of right wing extremist incidents happening every single day in Berlin and to maybe find interesting patterns by visualizing the data.

## The data
As already mentioned above, the data we used is provided by a non-governmental organization called [ReachOut](http://www.reachoutberlin.de), which is a counselling center for victims of rightwing extremist, racist or anti-semitic violence in Berlin.

There's also a little section on their page called „Chronicle“ where such violent incidents are documented and scaled in different folders by years from 2005 up until 2014.

The data is presented in tables as follows:

-------------------------------------------------------------------------------------------------------------------
| date and district         | incident description                                                                |
----------------------------|--------------------------------------------------------------------------------------
| 2013-09-09 Berlin-Wedding | Gegen 19.10 Uhr wird ein 23-jähriger Transsexueller in der Reinickendorfer Str[...] |
-------------------------------------------------------------------------------------------------------------------

## Get the data
The first step obviously was to get the data off of their page. For that purpose we wrote a scraper in python 3 which extracts the necessary contents from their HTML tables using the [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) library ([scraper.py](scraper/scraper.py)). The extracted data was inserted into a table called *Article* with the columns *ID*, *Date*, *Place* and *description* of a SQLite database.

This basically gave us the date of the incident, the district where the incident occured and a brief description of the incident in general.

## More precise locations
To visualize the incidents on a map, the district on its own seemed to be an imprecise basis. This is why we decided to analyze the description text of each incident to acquire further location information, since most of the description does contain such. To be able to identify possible locations within a continous text we used the Part-Of-Speech Tagger from the [Natural Language Toolkit](http://www.nltk.org/) (NLTK) which assigns parts of speech to each word, such as noun, verb and adjective ([analyze.py](analyze.py)). By having these tags assigned to each word we can go through the text and extract those nouns and names that happen to appear after a preposition (the tags *APPR* and *APPRART*). We defined these to be most likely further information on the incident location such as train stations and street names.

Doing this we realized that some of the words we extracted from the text were actually completely irrelevant (*hair*, *face*, *woman*, *evening* and the like). We supposed to be able to identify these irrelevant ones by simply querying a german dictionary whether it contains this word or not, to tell whether this word is a relevant location or just an irrelevant noun from the german language. We ended up checking a text file, containing around 24,000 german nouns.

## Categorizing incidents
As we examined some of the incident descriptions we came to the conclusion that it is possible to group most of the incidents by certain categories. We recognized four major categories: *homophic* incidents, *antisemtitic* incidents, *sexist* incidents and *racist* incidents. To automatically assign distinctive categories to each incident we implemented a simple algorithm which searches for certain keywords in the incident description. This way an incidents can be tagged with none or multiple categories ([analyze.py](analyze.py)). We stored these assignements in a seperate table of our SQLite database called *category* with the columns *ID*, *Name* and *Article_ID*.

```
bad_words = {
        'antisemit': 'antisemitism',
        'jud': 'antisemitism',
        'jüd': 'antisemitism',
        'homo': 'homophobia',
        'schwul': 'homophobia',
        'lesb': 'homophobia',
        'trans': 'homophobia',
        'sexis': 'sexism',
        'frauenfeind': 'sexism',
        'rassis': 'racism',
        'fremdenfeind': 'racism',
        'flüchtling': 'racism',
        'migrant': 'racism'
    }
```

## Geocoding
The extracted places of a description text may look like this.
```
[[('Berlin', 'NE'), ('Wedding', 'NE')], [('Bahnhof', 'NN'), ('Osloer', 'ADJA'), ('Straße', 'NN')]]
```

You can see each word and its corresponding tag. The places found in this particular description are **Berlin Wedding** and **Bahnhof Osloer Straße**.

To map things on a certain position on a map you need to have their longitude and latitude coordinates. To get these coordinates from the name of a place, one can use one of the numerous geocoding API's out there. The challenging part was having multiple possible places for one incident, so we needed the API to rate the precision of the things we pass to it. To stick with the example above: The first place **Berlin Wedding** is just the district where the incident occured and the second place is the train station which would be much more interesting to map.

Google's Geocoding API luckily offered this to us. Google's API can actually differentiate between the location types *ROOFTOP*, *RANGE_INTERPOLATED*, *GEOMETRIC_CENTER* and *APPROXIMATE* (descending precision) ([analyze.py](analyze.py)). That gave us the possibility to always pick the most precise location from our database, where we stored all locations inside a new table called *location* with the columns *ID*, *Confidence*, *Lat*, *Lng* and *Article_ID*.

## Visualization
To make our data accessible to the outside world we realized a very simple API with only one access route in python using a Web Server Gateway Interface (WSGI) framework called [bottle](http://bottlepy.org/docs/dev/index.html). This access route executes SQL queries to our database to get all incidents, all corresponding locations and their categories and wraps them into an array of JSON objects ([server.py](server.py)) and returns it.

To eventually visualize the data on a map we used the open-source JavaScript library [Leaflet](http://leafletjs.com/) in combination with [OpenStreetMap](http://www.openstreetmap.org/#map=5/51.500/-0.100) ([static/js](static/js)). For each incident a circle-marker is drawn with a specific color presenting its category, on a specific location and can be clicked for a small popup to present the incident description and the date when it occured.

## Problems we faced
### Textfile of german nouns
As described in the chapter **More precise locations** we used a text file containing numerous german nouns, to filter out irrelevant words. The problem we faced was, that we had to create this file all on our own by crawling the [Wiktionary](http://en.wiktionary.org/w/index.php?title=Category%3AGerman_nouns) page and scraping the contents of the category *German nouns*. We just couldn't find anything out of the box that we could have used for our specific needs.

### Filtering irrelevant words
Our algorithm at the moment discards words which appear in the german noun list. As already described, such words can be *face* or *woman*. The discarding process works fine for singular word cases, but as soon as they appear in plural they do not match with any nouns in the list anymore and therefore wrongly pass the filter anyway. This is why we had to clean some of the entries in our database by hand afterwards.

### Mapping incidents
Quite a lot of the incidents are mapped to the same position, which leads to a stack of markers that leaves markers below unreachable for the user to click. In order to avoid this bug we chose to use the [markercluster](https://github.com/Leaflet/Leaflet.markercluster) plugin which allows spiderfying a cluster of markers when it is clicked.

<!-- In order to set up the tables you have to create them first. This is done quite easily using the `python` interpreter:
```python
from models import *
create_tables()
``` -->