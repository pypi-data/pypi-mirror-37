# /usr/bin/env python
# -*- coding:utf-8 -*-

try:
    import queue
except ImportError:
    import Queue as queue
try:
    import asyncio
except ImportError:
    import trollius as asyncio

import logging

from asyncall.util import Result

logger = logging.getLogger(__name__)


@asyncio.coroutine
def _work(task, result_queue, no_result, all_result):
    try:
        result = yield asyncio.From(task)
    except Result as e:
        result = e.result
    except Exception as e:
        import traceback
        logger.warning('async exception: {e}\n {trace}'.format(e=e, trace=traceback.format_exc()))
        result = None

    if no_result:
        return
    if all_result:
        result_queue.put(result)
    else:
        if result:
            result_queue.put(result)
