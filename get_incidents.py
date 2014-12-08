# This file contains the logic that periodically fetches all pages on the
# Reachout Berlin homepage, checks if they're already in the database and inserts
# them if needed.

import sqlite3
import hashlib
import time
from scraper.scraper import Scraper

encoding = 'UTF-8'

# helper function for benchmarking
current_milli_time = lambda: int(round(time.time() * 1000))

#
# this is where the logic starts:
#

print('Start crawling…')
start_time = current_milli_time()
scraper = Scraper()
articles = scraper.scrape()
time_taken = current_milli_time() - start_time
print('Found {} articles in {} ms'.format(len(articles), time_taken))

conn = sqlite3.connect('violence.db')
c = conn.cursor()

# setup database schema
c.execute('PRAGMA encoding = "{}"'.format(encoding))

c.execute('''
    CREATE TABLE IF NOT EXISTS incidents (
        incident_id INTEGER PRIMARY KEY,
        date TEXT,
        month_only INTEGER,
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
        date, month_only, place, additional_place, description, hash
    ) VALUES (?,?,?,?,?,?)
'''

print('Starting database work')
for article in articles:
    # build a hash so we can more easily find out if we have an article already
    h = hashlib.sha256()
    h.update(str(article['date']).encode(encoding))
    h.update(article['place'].encode(encoding))
    h.update((article['additional_place'] or '').encode(encoding))
    h.update(article['description'].encode(encoding))
    digest = h.digest()

    c.execute(select_query, (digest,))

    # now if it's not in the database insert it
    if (not c.fetchone()):
        article_tuple = (
            article['date'],
            article['month_only'],
            article['place'],
            article['additional_place'],
            article['description'],
            digest
        )
        c.execute(insert_query, article_tuple)

final_time = current_milli_time() - start_time
print('All done in {} ms'.format(final_time))
