from nltk.tag.stanford import POSTagger
from models import Article

tagger = POSTagger('./stanford-postagger-full-2014-10-26/models/german-fast.tagger',
                   './stanford-postagger-full-2014-10-26/stanford-postagger-3.5.0.jar',
                    'UTF-8')

for article in Article.select().limit(100):
    pos = tagger.tag((article.place + " " + article.description).split())

    # extract the places
    places = []
    is_matching = False
    current_match = []
    for tuple in pos:
        if is_matching:
            # when we're matching, the phrases we're looking for look like
            # "Im S-Bahnhof Wedding"... the tags below mean
            if tuple[1] in ("ART", "ADJA", "NN", "NE", "CARD"):
                current_match.append(tuple)
            else:
                places.append(current_match)
                current_match = []
                is_matching = False
        else:
            # start matching when we have a preposition
            if tuple[1] in ("APPR", "APPRART"):
                is_matching = True

    print(article.place)
    print(article.description)
    print()
    print("Relevant: " + str(places))
