import bottle
import sqlite3
import json

@bottle.get("/")
def index():
    return bottle.template('index')

# @bottle.get("/locations/<article_id:int>")
# def location(article_id):
#     return (Location
#         .select()
#         .where(Location.article == article_id)
#         .order_by(Location.confidence.desc(), Location.id.asc())
#         .dicts()
#         .get())

# @bottle.get("/categories/<article_id:int>")
# def category(article_id):
#     categories = (Category
#         .select()
#         .where(Category.article == article_id))

#     return {
#         "article": article_id,
#         "categories": [c.name for c in categories]
#     }

@bottle.get("/articles/")
def articles():
    conn = sqlite3.connect('violence.db')
    c = conn.cursor()
    c = c.execute("""
                        SELECT  article.id, article.date, article.place, article.description, category.name,
                                location.confidence, location.lat, location.lng, location.match, location.returned_place
                        FROM    article
                            JOIN category ON article.id = category.article_id
                            JOIN location ON article.id = location.article_id
                  """)

    articles = []
    for article in c.fetchall():
        articles.append({
            "id":       article[0],
            "date":     article[1],
            "place":    article[2],
            "desc":     article[3],
            "cat":      article[4],
            "conf":     article[5],
            "lat":      article[6],
            "lng":      article[7],
            "match":    article[8],
            "returned_place": article[9]
        })
    conn.close()
    return json.dumps(articles)

@bottle.get('/static/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root='static/')

if __name__ == "__main__":
    bottle.run(host="localhost", port=12345, reloader=True, debug=True)
