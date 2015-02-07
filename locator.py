import time
from models import *
from analyze import *

print("Start geocoding...")
start_time = time.time()
articles = Article.select().where(Article.id < 701)

# use our list of german nouns for filtering
with open("german_nouns.txt", "r") as f:
    german_nouns = f.read().splitlines()

for article in articles:
    potential = get_potential_places(article.place, article.description)
    places = improve_potential_places(potential)

    print("Found places: {}".format(places))

    for place in places:
        query = " ".join([word for (word, tag) in place])
        if query in german_nouns:
            print("Skipping {}".format(query))
        else:
            print("Query: {}, Berlin".format(query))

            locations = get_geoloc(query)

            # TODO: Only insert matches that have a higher confidence than current
            # ones
            for location in locations:
                location["article"] = article
                location["match"] = query
                Location.create(**location)

            time.sleep(1)

time_taken = time.time() - start_time
print("Geocoded {} articles in {} seconds".format(articles.count(), time_taken))
