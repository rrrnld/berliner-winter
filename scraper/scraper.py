from bs4 import BeautifulSoup
from urllib import parse, request
from datetime import date

class Scraper():

    def __init__(self, index='http://www.reachoutberlin.de/modules.php?op=modload&name=topics&file=index&cm=9&cb=8'):
        parsed_url = parse.urlparse(index)

        self.start = request.urlopen(index)
        self.base_url = parsed_url.scheme + "://" + parsed_url.netloc

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
            # headlines are always YYYY-MM-DD Berlin-DISTRICT (+ sometimes additional info)
            headline = table.select('tr:first-child')[0].get_text()

            year, month, day = headline[:headline.find(' ')].strip().split('-')
            places = headline[headline.find(' ') + 1:]

            if places.find(' ') == -1:
                district = places
                additional = None
            else:
                district = places[:places.find(' ')]
                additional = places[places.find(' ') + 1:].strip()

            text = table.select('tr')[2].select('td')[1].get_text()

            article = {
                'date': date.strip(),
                'place': district,
                'additional_place': additional,
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
            currentDoc = BeautifulSoup(request.urlopen(url))

            while currentDoc:
                new_articles = self.get_articles_on_page(currentDoc)
                articles.extend(new_articles)
                currentDoc = self.get_next_page(currentDoc)

        return articles
