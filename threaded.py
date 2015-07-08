import io
import requests
import threading
import time

from lxml import etree


COMPANIES = {
    # Ticker symbol -> Glassdoor page
    'GOOGL': 'Google-Reviews-E9079.htm',
    'AAPL': 'Apple-Reviews-E1138.htm',
    'FB': 'Facebook-Reviews-E40772.htm'
}


def get_PE(symbol):
    url = 'http://www.google.com/finance?q=NASDAQ%%3A%s' % symbol
    response = requests.get(url)

    # Parse HTML response
    tree = etree.parse(io.BytesIO(response.content), etree.HTMLParser())
    return float(tree.xpath('//td[@data-snapfield="pe_ratio"]/following-sibling::td/text()')[0].strip())  # noqa


def get_glassdoor_rating(symbol):
    page_name = COMPANIES[symbol]
    url = 'http://www.glassdoor.com/Reviews/%s' % page_name
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'  # noqa
    })

    # Parse HTML response
    tree = etree.parse(io.BytesIO(response.content), etree.HTMLParser())
    return float(tree.xpath('//div[@class="notranslate ratingNum"]/text()')[0])


def compute_PEG(symbol):
    return get_PE(symbol) / get_glassdoor_rating(symbol)


class PegThread(threading.Thread):

    def __init__(self, symbol):
        super(PegThread, self).__init__()
        self.symbol = symbol

    def run(self):
        peg = compute_PEG(self.symbol)
        print('%s\t%5.2f' % (self.symbol, peg))


def main():
    start = time.time()

    threads = []
    for symbol in COMPANIES:
        t = PegThread(symbol)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print('Done: %.2f sec' % (time.time() - start))

main()
