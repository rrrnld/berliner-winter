from bs4 import BeautifulSoup
from urllib import parse, request
from datetime import date
import re

class Scraper():

    def __init__(self, index='http://www.reachoutberlin.de/modules.php?op=modload&name=topics&file=index&cm=9&cb=8'):
        parsed_url = parse.urlparse(index)

        self.start = request.urlopen(index)
        self.base_url = parsed_url.scheme + "://" + parsed_url.netloc

        # dates are a bit dificult; usually they're formatted like YYYY-MM-DD,
        # followed by a space character, but sometimes the day is missing or it's
        # followed by another character…
        self.date_matcher = re.compile('^(\d{4})-(\d{,2})(-(\d{,2}))?')

    def get_next_page(self, document):
        nav_elem = document.select('.nav')[1]

        if nav_elem.get_text().strip() == '>':
            href = nav_elem.get('href')
            return BeautifulSoup(request.urlopen(href))
        else:
            return None


    def get_articles_on_page(self, document):
        article_tables = document.select('table[width="98%"]')
        articles = []

        for table in article_tables:
            # headlines are always YYYY-MM-DD? Berlin-DISTRICT (+ sometimes additional info)
            headline = table.select('tr:first-child')[0].get_text()

            date_match = self.date_matcher.match(headline.strip())

            try:
                year, month, day = date_match.group(1,2,4)
            except:
                print('Failed for headline ' + headline)
                raise

            place = headline[headline.find(' ') + 1:]

            text = table.select('tr')[2].select('td')[1].get_text()

            article = {
                'date': date(int(year), int(month), int(day) if day else 1),
                'month_only': day is None,
                'place': place.strip(),
                'description': text.strip()
            }
            articles.append(article)

        return articles

    def get_yearly_overviews(self):
        document = BeautifulSoup(self.start)
        links = document.find_all('a')
        overviews = []

        for link in links:
            if link.get_text().lower().startswith('chronik'):
                overview_link = link.get('href')
                overviews.append(parse.urljoin(self.base_url, overview_link))

        return overviews

    def scrape(self):
        overview_urls = self.get_yearly_overviews()
        articles = []

        for url in overview_urls:
            current_doc = BeautifulSoup(request.urlopen(url))

            while current_doc:
                new_articles = self.get_articles_on_page(current_doc)
                articles.extend(new_articles)
                current_doc = self.get_next_page(current_doc)

        return articles
