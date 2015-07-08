import asyncio
import time


PE = {
    'GOOGL': 27.08,
    'AAPL': 15.58,
    'FB': 87.34
}

GLASSDOOR = {
    'GOOGL': 4.4,
    'AAPL': 4.0,
    'FB': 4.5
}


@asyncio.coroutine
def get_PE(symbol):
    yield from asyncio.sleep(2)
    return PE[symbol]


@asyncio.coroutine
def get_glassdoor_rating(symbol):
    yield from asyncio.sleep(2)
    return GLASSDOOR[symbol]


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
    tasks = [print_PEG(symbol) for symbol in PE]
    loop.run_until_complete(asyncio.wait(tasks))

    print('Done: %.2f sec' % (time.time() - start))


main()
