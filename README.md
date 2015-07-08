# Python 3.4 asyncio Demo

Source code for https://speakerdeck.com/eliang/asynchronous-python

## Unmocked Version

These scripts really send HTTP requests to Google Finance and Glassdoor to get
stock quotes and company ratings.

* `sync.py` - Synchronous implementation
* `threaded.py` - Threaded implementation
* `coroutine.py` - Coroutine implmentation using asyncio
* `coroutine2.py` - Improved coroutine implmentation

## Mocked Version

These are basically the same with their unmocked versions, except for they
simulate HTTP requests with `sleep`. So we can have a more predictable
execution time.

* `mocked_sync.py`
* `mocked_threaded.py`
* `mocked_coroutine.py`
* `mocked_coroutine2.py`
