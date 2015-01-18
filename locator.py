import time
from models import *
from analyze import *

print("Start geocoding...")
start_time = time.time()
articles = Article.select()

for article in articles:
    potential = get_potential_places(article.place, article.description)
    places = improve_potential_places(potential)

    print("Found places: {}".format(places))

    for place in places:
        query = " ".join([word for (word, tag) in place])
        print("Query: {}, Berlin".format(query))

        locations = get_geoloc(query)

        for location in locations:
            location["article"] = article
            location["match"] = query
            Location.create(**location)

        time.sleep(1)

time_taken = time.time() - start_time
print("Geocoded {} articles in {} seconds".format(articles.count(), time_taken))
