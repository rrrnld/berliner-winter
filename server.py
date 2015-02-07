import bottle
import sqlite3
import json

@bottle.get("/")
def index():
    return bottle.template('index')

@bottle.get("/articles/")
def articles():
    conn = sqlite3.connect('violence.db')
    cursor = conn.cursor()

    l = cursor.execute("""
                        SELECT  location.lat, location.lng, location.returned_place, location.article_id
                        FROM    location
                        ORDER BY location.confidence DESC, location.id ASC
                       """)

    locations = {}
    for location in l.fetchall():
        # check if we already have entries for the article_id
        if not locations.get(location[3]):
            locations[location[3]] = (location[0], location[1], location[2])

    c = cursor.execute("""
                        SELECT  article.id, article.date, article.place, article.description, category.name
                        FROM    article
                            LEFT OUTER JOIN category ON article.id = category.article_id
                       """)

    articles = {}
    for article in c.fetchall():
        article_id = article[0]
        if locations.get(article_id):
            if articles.get(article_id):
                articles[article_id]["categories"].append(article[4])
            else:
                articles[article_id] = {
                    "id":           article_id,
                    "date":         article[1],
                    "place":        article[2],
                    "description":  article[3],
                    "categories":   [article[4]],
                    "lat":          locations[article_id][0],
                    "lng":          locations[article_id][1],
                    "place":        locations[article_id][2]
                }
    conn.close()

    return json.dumps([article for article_id, article in articles.items()])

@bottle.get('/static/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root='static/')

if __name__ == "__main__":
    bottle.run(host="localhost", port=12345, reloader=True, debug=True)
