#coding=utf-8

from functools import wraps
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
class coming():
    def __init__(self,future,timeout):
        self.__future = future
        self.__timeout = timeout

    def __getattr__(self,name):
        ret = self.__wait()
        return ret.__getattribute__(name)

    def __wait(self):
        return self.__future.result(self.__timeout)
    
def async(n, base_type, timeout=None):
    def decorator(f):
        if isinstance(n, int):
            pool = base_type(n)
        elif isinstance(n, base_type):
            pool = n
        else:
            raise TypeError(
                "Invalid type: %s"
                % type(base_type)
            )
        @wraps(f)
        def wrapped(*args, **kwargs):
            return coming(
                pool.submit(f, *args, **kwargs),  # 创建future对象
                timeout=timeout
            )
        return wrapped
    return decorator


def threads(n, timeout=None):
    return async(n, ThreadPoolExecutor, timeout)


# import time
# import requests

# @threads(5,2)
# def download(url):
#     return requests.get(url)
# def download2(url):
#     return requests.get(url)

# if __name__ == "__main__":
#     urls = ['http://www.baidu.com','http://www.sohu.com','http://www.qq.com']
#     start = time.time()
#     responses = [download(url) for url in urls]
#     html = [response.text for response in responses]
#     end = time.time()
#     print "Time: %f seconds" % (end - start)