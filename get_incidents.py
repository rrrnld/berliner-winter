# This file contains the logic that periodically fetches all pages on the
# Reachout Berlin homepage, checks if they're already in the database and inserts
# them if needed.

import sqlite3
import hashlib
from scraper.scraper import Scraper

encoding = 'utf-8'

scraper = Scraper()
articles = scraper.scrape()

conn = sqlite3.connect('violence.db')
c = conn.cursor()

# setup database schema
c.execute('''
    CREATE TABLE IF NOT EXISTS incidents (
        incident_id INTEGER PRIMARY KEY,
        date TEXT,
        place TEXT,
        additional_place TEXT,
        description TEXT,
        hash
    );
''')

c.execute('''
    CREATE INDEX IF NOT EXISTS incidents_date
    ON incidents (date);
''')

c.execute('''
    CREATE INDEX IF NOT EXISTS incidents_hash
    ON incidents (hash);
''')

# insert articles if necessary
select_query = 'SELECT * FROM incidents WHERE hash=?'
insert_query = '''
    INSERT INTO incidents (
        date, place, additional_place, description, hash
    ) VALUES (?)
'''
for article in articles:
    # build a hash so we can more easily find out if we have an article already
    h = h.sha256()
    h.update(article.date.encode(encoding))
    h.update(article.place.encode(encoding))
    h.update(article.additional_place.encode(encoding))
    h.update(article.description.encode(encoding))
    digest = h.digest()

    c.execute(select_query)

    if (not c.fetchone()):
        article_tuple = (
            article.date,
            article.place,
            article.additional_place,
            article.description,
            digest
        )
        c.execute(insert_query, article_tuple)
