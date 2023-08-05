# /usr/bin/env python
# -*- coding:utf-8 -*-

from tests.context import Result
import asyncio

# @asyncio.coroutine
# def demo(name):
#     import random
#     asleep = random.randint(0, 1)
#     print('---start, %s  %s' % (name, asleep))
#     yield from asyncio.sleep(asleep)
#     print('---stop, %s' % name)
#     # raise Result(name)
#     return name

async def demo(name):
    import random
    asleep = random.randint(0, 1)
    print('---start, %s  %s' % (name, asleep))
    await asyncio.sleep(asleep)
    print('---stop, %s' % name)
    # raise Result(name)
    return name