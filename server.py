import bottle
from json import dumps
from models import *

@bottle.get('/locations/<article_id:int>')
def location(article_id):
    return (Location
        .select()
        .where(Location.article == article_id)
        .order_by(Location.confidence.desc(), Location.id.asc())
        .dicts()
        .get())

if __name__ == '__main__':
    bottle.run(host='localhost', port=12345, reloader=True, debug=True)
