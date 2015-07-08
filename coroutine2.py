import aiohttp
import asyncio
import io
import time

from lxml import etree


COMPANIES = {
    # Ticker symbol -> Glassdoor page
    'GOOGL': 'Google-Reviews-E9079.htm',
    'AAPL': 'Apple-Reviews-E1138.htm',
    'FB': 'Facebook-Reviews-E40772.htm'
}


@asyncio.coroutine
def get_PE(symbol):
    url = 'http://www.google.com/finance?q=NASDAQ%%3A%s' % symbol
    response = yield from aiohttp.request('GET', url)
    data = yield from response.read()

    # Parse HTML response
    tree = etree.parse(io.BytesIO(data), etree.HTMLParser())
    return float(tree.xpath('//td[@data-snapfield="pe_ratio"]/following-sibling::td/text()')[0].strip())  # noqa


@asyncio.coroutine
def get_glassdoor_rating(symbol):
    page_name = COMPANIES[symbol]
    url = 'http://www.glassdoor.com/Reviews/%s' % page_name
    response = yield from aiohttp.request('GET', url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'  # noqa
    })
    data = yield from response.read()

    # Parse HTML response
    tree = etree.parse(io.BytesIO(data), etree.HTMLParser())
    return float(tree.xpath('//div[@class="notranslate ratingNum"]/text()')[0])


@asyncio.coroutine
def compute_PEG(symbol):
    pe, g = yield from asyncio.gather(
        get_PE(symbol), get_glassdoor_rating(symbol))
    return pe / g


@asyncio.coroutine
def print_PEG(symbol):
    peg = yield from compute_PEG(symbol)
    print('%s\t%5.2f' % (symbol, peg))


def main():
    start = time.time()

    loop = asyncio.get_event_loop()
    tasks = [print_PEG(symbol) for symbol in COMPANIES]
    loop.run_until_complete(asyncio.wait(tasks))

    print('Done: %.2f sec' % (time.time() - start))


main()
