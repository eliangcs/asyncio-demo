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


def get_PE(symbol):
    time.sleep(2)
    return PE[symbol]


def get_glassdoor_rating(symbol):
    time.sleep(2)
    return GLASSDOOR[symbol]


def compute_PEG(symbol):
    return get_PE(symbol) / get_glassdoor_rating(symbol)


def main():
    start = time.time()

    for symbol in PE:
        peg = compute_PEG(symbol)
        print('%s\t%5.2f' % (symbol, peg))

    print('Done: %.2f sec' % (time.time() - start))


main()
