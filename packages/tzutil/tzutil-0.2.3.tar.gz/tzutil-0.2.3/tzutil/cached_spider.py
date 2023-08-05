#!/usr/bin/env python

from tzutil.cached_req import Req
from tzutil.spider import Spider

class CachedSpider(Spider):
    def __init__(self, path, expire=None, vaild=lambda html:1, *args, **kwds):

        super(CachedSpider, self).__init__(
            *args, **kwds
        )
        self._get = Req(path, expire, vaild).async_get



