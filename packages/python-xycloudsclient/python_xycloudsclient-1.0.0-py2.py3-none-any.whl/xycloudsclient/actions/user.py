#!-*- coding:utf8 -*-
import weakref
from xycloudsclient.common import get_config


class UserManager(object):

    def __init__(self, client):
        self.conn = weakref.proxy(client)
        self.endpoint = get_config('region_url', 'account')
        self.url_prex = '/user/'

    def show_regions(self):
        url = 'regions'
        result = self.conn.do_request('GET', url,
                                      endpoint=self.endpoint,
                                      url_prex=self.url_prex)
        return result

    def show_basic(self):
        url = 'account'
        result = self.conn.do_request('GET', url,
                                      endpoint=self.endpoint,
                                      url_prex=self.url_prex)
        return result
