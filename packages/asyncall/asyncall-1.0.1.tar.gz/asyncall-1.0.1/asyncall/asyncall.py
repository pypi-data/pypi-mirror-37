# /usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import types

try:
    import queue
except ImportError:
    import Queue as queue
try:
    import asyncio
except ImportError:
    import trollius as asyncio

if '2' == sys.version[0]:
    from .adaptive.python2 import _work

    coroutine_type = types.GeneratorType
else:
    from .adaptive.python3 import _work

    coroutine_type = (types.GeneratorType, types.CoroutineType)


class AsyncManage(object):

    def __init__(self, loop=None):
        super(AsyncManage, self).__init__()
        self._loop = loop if loop else asyncio.get_event_loop()
        self._result_queue = queue.Queue()

    def imap(self, tasks):
        no_result = False
        all_result = True
        while tasks:
            tasks.reverse()
            task = tasks.pop()
            items = self._run(task, no_result=no_result, all_result=all_result)
            self._loop.run_until_complete(asyncio.wait(items))
            result = self._result_queue.get_nowait()
            yield result

    def map(self, tasks):
        no_result = False
        all_result = True
        self.run(tasks, no_result=no_result, all_result=all_result)
        return [self._result_queue.get_nowait() for _ in range(len(tasks))]

    def _wrap_task(self, task):
        return asyncio.ensure_future(task)

    def wrap_task(self, *args):
        items = []
        for task in args:
            if not isinstance(task, coroutine_type):
                raise TypeError
            items.append(self._wrap_task(task))
        return items

    def _run(self, tasks, no_result=True, all_result=True):
        items = []
        if isinstance(tasks, coroutine_type):
            task = _work(task=tasks, result_queue=self._result_queue, no_result=no_result, all_result=all_result)
            items.extend(self.wrap_task(task))
        elif isinstance(tasks, list):
            for task in tasks:
                if isinstance(task, coroutine_type):

                    task = _work(task=task, result_queue=self._result_queue, no_result=no_result,
                                 all_result=all_result)
                    items.append(task)
                else:
                    raise TypeError
            items = self.wrap_task(*items)
        else:
            raise TypeError
        return items

    def run(self, tasks, no_result=True, all_result=True):
        items = self._run(tasks, no_result, all_result)
        self._loop.run_until_complete(asyncio.wait(items))


class AsyncTaskManage:

    def __init__(self, async_func, loop=None):
        self._async_manage = AsyncManage(loop)
        self._async_func = async_func

    def _wrapper_para(self, tasks):
        items = []
        for task in tasks:
            if isinstance(task, (list, tuple)):
                items.append(self._async_func(*task))
            elif isinstance(task, dict):
                items.append(self._async_func(**task))
            else:
                items.append(self._async_func(task))
        return items

    def imap(self, tasks):
        tasks = self._wrapper_para(tasks)
        task_generator = self._async_manage.imap(tasks)
        while tasks:
            yield next(task_generator)

    def map(self, tasks):
        tasks = self._wrapper_para(tasks)
        return self._async_manage.map(tasks)

    def run(self, tasks):
        tasks = self._wrapper_para(tasks)
        self._async_manage.run(tasks)


def map(tasks, loop=None):
    am = AsyncManage(loop=loop)
    return am.map(tasks)


def imap(tasks, loop=None):
    am = AsyncManage(loop=loop)
    return am.imap(tasks)


def task_map(tasks, async_func, loop=None):
    atm = AsyncTaskManage(async_func, loop=loop)
    return atm.map(tasks)


def task_imap(tasks, async_func, loop=None):
    atm = AsyncTaskManage(async_func, loop=loop)
    return atm.imap(tasks)
