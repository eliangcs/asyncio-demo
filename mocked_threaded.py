import threading
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
    for symbol in PE:
        t = PegThread(symbol)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print('Done: %.2f sec' % (time.time() - start))

main()
