import bottle
from models import *

@bottle.get("/locations/<article_id:int>")
def location(article_id):
    return (Location
        .select()
        .where(Location.article == article_id)
        .order_by(Location.confidence.desc(), Location.id.asc())
        .dicts()
        .get())

@bottle.get("/categories/<article_id:int>")
def category(article_id):
    categories = (Category
        .select()
        .where(Category.article == article_id))

    return {
        "article": article_id,
        "categories": [c.name for c in categories]
    }

@bottle.get("/articles/<article_id:int>")
def article(article_id):
    # articles have a datetime field and need special serialization
    # return json_util.dumps(Article
    #     .select()
    #     .where(Article.id == article_id)
    #     .dicts()
    #     .get())
    pass

if __name__ == "__main__":
    bottle.run(host="localhost", port=12345, reloader=True, debug=True)
