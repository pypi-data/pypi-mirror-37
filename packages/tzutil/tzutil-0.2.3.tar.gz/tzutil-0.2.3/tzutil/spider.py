#!/usr/bin/env python
import json
import aiohttp
import asyncio
from urllib.parse import urlparse,ParseResult,parse_qsl,parse_qs
from tzutil.ob import Ob
import time

class Req:
    def __init__(self, url, html):
        self.__url = url
        self.text = html

    @property
    def ob(self):
        o = self.json
        return (Ob()<<o)

    @property
    def json(self):
        return json.loads(self.text)

    @property
    def parse_qs(self):
        return parse_qs(self.__url.query)

    @property
    def parse_qsl(self):
        return parse_qsl(self.__url.query)

    def __getattr__(self, attr):
        return getattr(self.__url, attr)


class Spider:
    def __init__(self, duration=20, headers={}, encode="utf-8"):
        self._todo = []
        self._timeout = 60
        self._costed = 0
        self.encode = encode
        self.headers = headers
        self._duration = 20
        self._func = []
        agent = "User-Agent"
        if agent not in headers:
            headers[agent] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"

    def get(self, url):
        self._todo.append(url)

    async def _get(self, url, headers):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                return await response.read()

    async def _run(self):
        duration = self._duration
        cached = 0.1
        cost = cached+1
        while 1:
            if self._todo:
                url = self._todo.pop()
                begin = time.time()
                html = await self._get(url, headers=self.headers)
                cost = time.time() - begin
                if not self._parse(url, html):
                    print("⚠️  %s 无内容抽取函数"%url)
            else:
                if self._costed > self._timeout:
                    return
                self._costed += duration
                print('爬虫抓取队列为空 %s秒'%self._costed)
            if cost > cached: # 表示没缓存
                await asyncio.sleep(duration)

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._run())

    def _parse(self, url, html):
        if self.encode:
            html = html.decode('utf-8')
        url = urlparse(url)
        run = lambda : func(Req(url,html))
        for pattern, func in self._func:
            if pattern:
                p = pattern.get('path')
                if p:
                    path = url.path[1:]
                    pathb = path.encode('utf-8')
                    if type(p) is bytes:
                        if pathb.startswith(p):
                            run()
                            return 1
            else:
                run()
                return 1

    def __call__(self, *args, **kwds):
        if args:
            self._func.append((None, args[0]))
            return
        def _(func):
            self._func.append((kwds, func))
            return func
        return _

