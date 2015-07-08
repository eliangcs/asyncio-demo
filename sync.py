import io
import requests
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


def main():
    start = time.time()

    for symbol in COMPANIES:
        peg = compute_PEG(symbol)
        print('%s\t%5.2f' % (symbol, peg))

    print('Done: %.2f sec' % (time.time() - start))


main()
