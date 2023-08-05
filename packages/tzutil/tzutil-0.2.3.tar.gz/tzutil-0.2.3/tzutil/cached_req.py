#!/usr/bin/env python
import aiohttp
import rocksdb
from time import time
import requests
from urllib.parse import urlparse
from os.path import join
from json import loads
from tzutil.req import get
import pathlib
import struct


class Req:
    def __init__(self, path, expire=None, valid=lambda html:1):
        self._path = path
        self.expire = expire
        self.valid = valid
        self.__db = {}
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)


    def _db(self, name):
        _db = self.__db
        db = _db.get(name)
        if not db:
            db = _db[name] = rocksdb.DB(
                join(self._path, name), rocksdb.Options(create_if_missing=True)
            )
        return db

    def _cached(self, url):
        db = self._db(urlparse(url).netloc)
        _url = url.encode('utf-8')
        now = int(time())
        r = db.get(_url)
        if r:
            html = r[8:]
            if self.valid(html):
                expire = self.expire
                if expire:
                    cache_time = struct.unpack("Q", r[:8])[0]
                    if (now -cache_time) < expire:
                        return html
                else:
                    return html
        def put( html):
            db.put(_url, struct.pack('Q',now)+html)
        return put

    def get(self, url, *args, **kwds):

        html = self._cached(url)

        if type(html) is bytes:
            return html
        else:
            _put = html
        html = get(url, *args, **kwds)
        if not html:
            return
        html = html.content
        _put(html)
        return html

    async def async_get(self, url, *args, **kwds):
        html = self._cached(url)

        if type(html) is bytes:
            return html
        else:
            _put = html

        async with aiohttp.ClientSession(headers=kwds.get('headers')) as session:
            async with session.get(url) as response:
                html = await response.read()
                _put(html)
                return html

