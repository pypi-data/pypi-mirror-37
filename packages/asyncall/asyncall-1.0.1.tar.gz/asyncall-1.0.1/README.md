# asyncall  -- 更加简单方便的异步调用方式


# 特性
1. 支持 python2 和 python3
2. 更加方便的异步调用方式
3. 支持惰性获取结果

# 用法
```
>>> import asyncio
>>> import asyncall
>>> async def demo(para):
...     await asyncio.sleep(1)
...     return para
...
>>> paras = ['A', 'B', 'C']
>>> res = asyncall.task_map(paras, async_func=demo)
>>>
>>> res
['A', 'B', 'C']
```
详见 tests/test_async.py

# 注意
1. python2 需要安装相关第三方库（requirements.txt）
