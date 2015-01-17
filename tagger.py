from nltk.tag.stanford import POSTagger
from models import Article
from analyze import *

tagger = POSTagger('./stanford-postagger-full-2014-10-26/models/german-fast.tagger',
                   './stanford-postagger-full-2014-10-26/stanford-postagger-3.5.0.jar',
                    'UTF-8')

for article in Article.select().limit(100):
    potential = get_potential_places(article.place, article.description)
    places = improve_potential_places(potential)

    print(article.place)
    print(article.description)
    print()
    print("Potential: " + str(potential))
    print("Improved:  " + str(places))
