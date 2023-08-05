# /usr/bin/env python
# -*- coding:utf-8 -*-

from tests.context import Result
import random

try:
    import asyncio
except ImportError:
    import trollius as asyncio

@asyncio.coroutine
def demo(name):
    asleep = random.randint(0, 1)
    print('---start, %s  %s' % (name, asleep))
    yield asyncio.sleep(asleep)
    print('---stop, %s' % name)
    raise Result(name)
