from bs4 import BeautifulSoup
from urllib import parse, request

class Scraper():

    def __init__(self, index='http://www.reachoutberlin.de/modules.php?op=modload&name=topics&file=index&cm=9&cb=8'):
        parsed_url = parse.urlparse(index)

        self.start = request.urlopen(index)
        self.base_url = parsed_url.scheme + "://" + parsed_url.netloc

    def has_more_pages(self):
        pass

    def visit_next_page(self):
        pass

    def get_articles_on_page(self, url):
        document = BeautifulSoup(request.urlopen(url))
        article_tables = document.select('table[width="98%"]')
        articles = []

        for table in article_tables:
            # headlines are always YYYY-MM-DD Berlin-DISTRICT (+ sometimes additional info)
            headline = table.select('tr:first-child')[0].get_text()

            date = headline[:headline.find(' ')]
            places = headline[headline.find(' ') + 1:]

            if places.find(' ') == -1:
                district = places
                additional = None
            else:
                district = places[:places.find(' ')]
                additional = places[places.find(' ') + 1:]

            text = table.select('tr:nth-of-type(3)')[0].select('td:nth-of-type(2)')[0].get_text()

            article = {
                'date': date.strip(),
                'place': district,
                'additional': additional,
                'text': text.strip()
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

        return self.get_articles_on_page(overview_urls[0])

        # for url in overview_urls:

        #     while self.has_more_pages():
        #         self.visit_next_page()
