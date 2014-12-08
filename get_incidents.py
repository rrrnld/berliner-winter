# This file contains the logic that periodically fetches all pages on the
# Reachout Berlin homepage, checks if they're already in the database and inserts
# them if needed.

import sqlite3
from scraper.scraper import Scraper

# scraper = Scraper()
# articles = scraper.scrape()

conn = sqlite3.connect('violence.db')
c = conn.cursor()

# setup database schema
c.execute('''
    CREATE TABLE IF NOT EXISTS incidents (
        incident_id INTEGER PRIMARY KEY,
        date TEXT,
        place TEXT,
        additional_place TEXT,
        description TEXT
    );
''')

c.execute('''
    CREATE INDEX IF NOT EXISTS incidents_date
    ON incidents (date);
''')

# insert articles
# for article in articles:
#     pass
