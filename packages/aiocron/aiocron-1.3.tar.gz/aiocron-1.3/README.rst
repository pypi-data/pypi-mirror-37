================================================
aiocron - Crontabs for asyncio
================================================

.. image:: https://travis-ci.org/gawel/aiocron.svg?branch=master
  :target: https://travis-ci.org/gawel/aiocron
.. image:: https://img.shields.io/pypi/v/aiocron.svg
  :target: https://pypi.python.org/pypi/aiocron
.. image:: https://img.shields.io/pypi/dm/aiocron.svg
  :target: https://pypi.python.org/pypi/aiocron

Usage
=====

``aiocron`` provide a decorator to run function at time::

    >>> @aiocron.crontab('*/30 * * * *')
    ... @asyncio.coroutine
    ... def attime():
    ...     print('run')
    >>> asyncio.get_event_loop().run_forever()

You can also use it as an object::

    >>> @aiocron.crontab('1 9 * * 1-5', start=False)
    ... @asyncio.coroutine
    ... def attime():
    ...     print('run')
    >>> attime.start()
    >>> asyncio.get_event_loop().run_forever()

Your function still be available at ``attime.func``

You can also yield from a crontab. In this case, your coroutine can accept
arguments::

    >>> @aiocron.crontab('0 9,10 * * * mon,fri', start=False)
    ... @asyncio.coroutine
    ... def attime(i):
    ...     print('run %i' % i)

    >>> @asyncio.coroutine
    ... def once():
    ...     try:
    ...         res = yield from attime.next(1)
    ...     except Exception as e:
    ...         print('It failed (%r)' % e)
    ...     else:
    ...         print(res)
    >>> asyncio.get_event_loop().run_forever()

Finally you can use it as a sleep coroutine. The following will wait until
next hour::

    >>> yield from crontab('0 * * * *').next()

If you don't like the decorator magic you can set the function by yourself::

    >>> cron = crontab('0 * * * *', func=yourcoroutine, start=False)

Notice that unlike standard unix crontab you can specify seconds at the 6th
position.

``aiocron`` use `croniter <https://pypi.python.org/pypi/croniter>`_. Refer to
it's documentation to know more about crontab format.

I've spent hours writing this software, with love.
Please consider tiping if you like it:

BTC: 1PruQAwByDndFZ7vTeJhyWefAghaZx9RZg

ETH: 0xb6418036d8E06c60C4D91c17d72Df6e1e5b15CE6

LTC: LY6CdZcDbxnBX9GFBJ45TqVj8NykBBqsmT
