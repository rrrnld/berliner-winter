# This file contains the logic that periodically fetches all pages on the
# Reachout Berlin homepage, checks if they're already in the database and inserts
# them if needed.

import sqlite3
import hashlib
import time
from models import *
from scraper.scraper import Scraper

encoding = 'UTF-8'

# helper function for benchmarking
current_milli_time = lambda: int(round(time.time() * 1000))

# First crawl through the whole index and get all articles we can find
print('Start crawling…')
start_time = current_milli_time()
scraper = Scraper()
articles = scraper.scrape()
time_taken = current_milli_time() - start_time
print('Found {} articles in {} ms'.format(len(articles), time_taken))

# Now fill the database
print('Starting database work')

for article in articles:
    # build a hash so we can more easily find out if we have an article already
    h = hashlib.sha256()
    h.update(str(article['date']).encode(encoding))
    h.update(article['place'].encode(encoding))
    h.update(article['description'].encode(encoding))
    digest = h.digest()

    try:
        Article.get(Article.hash == digest)
    except:
        # article not found
        Article.create(
            date = article['date'],
            month_only = article['month_only'],
            place = article['place'],
            description = article['description'],
            hash = digest
        )

final_time = current_milli_time() - start_time
print('All done in {} ms'.format(final_time))
