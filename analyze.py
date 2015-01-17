import re
import string
from nltk.tag.stanford import POSTagger

tagger = POSTagger('./stanford-postagger-full-2014-10-26/models/german-fast.tagger',
                   './stanford-postagger-full-2014-10-26/stanford-postagger-3.5.0.jar',
                    'UTF-8')

punctuation_regex = re.compile("[%s]" % re.escape(string.punctuation))

def get_potential_places(article_place, article_body):
    """
    Returns a list of potential places as tuples with their part-of-speech tags
    for later filtering
    """
    # remove punctuation
    full_text = punctuation_regex.sub(" ", article_place + " " + article_body)

    pos = tagger.tag(full_text.split())

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
                # we stop the match, so append the current match
                places.append(current_match)
                current_match = []
                is_matching = False
        else:
            # start matching when we have a preposition
            if tuple[1] in ("APPR", "APPRART"):
                is_matching = True

    return places

def improve_potential_places(pos_tuples):
    """
    Improves the matches' quality so we don't have to look up the lat-lng of so
    many mismatches
    """
    better_tuples = []
    for tuple_list in pos_tuples:
        # first, exluce empty lists
        if tuple_list:
            cleaner = []

            index = -1
            for tuple in tuple_list:
                index += 1

                # exclude articles ("the", "a"), they only introduce noise, but
                # keep the wh
                if tuple[1] is "ART":
                    continue

                # if we have numbers in the middle of our phrase, it's probably
                # also not useful (as opposed to Krügerstr. 22)
                if tuple[1] is "CARD" and index < len(tuple_list):
                    cleaner_tuple = []
                    break

                cleaner.append(tuple)

            better_tuples.append(cleaner)

    return better_tuples

def get_district(article_headline):
    """
    Returns a geo-coded version of a district an article is about, based on its
    headline.
    """
    pass

def get_categories(article_body):
    """
    Gives a list of categories an article falls into, which is empty if none of
    the following are matched:
    - sexism
    - antisemitism
    - homophobia
    - racism
    """
    bad_words = {
        'antisemit': 'antisemitism',
        'homophob': 'homophobia',
        'sexis': 'sexism',
        'rassis': 'racism'
    }
    found_categories = [bad_words[key] for key in bad_words
                                        if key in article_body.lower()]
    return found_categories or ['other']
