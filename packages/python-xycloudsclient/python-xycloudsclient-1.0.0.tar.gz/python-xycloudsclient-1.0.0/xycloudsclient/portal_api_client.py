#!-*- coding:utf8 -*-
import json
import md5
import random
import requests
import string
import time
from datetime import datetime
from xycloudsclient import exceptions
from xycloudsclient.common import filter_out_none, \
    get_config, update_config, get_data


class XycloudsPortalApiClient(object):

    def __init__(self, app_id=None, app_secret=None, endpoint=None,
                 ssl_verify=True, retries=1, timeout=300, proxies=None):
        """Xyclouds portal api access sdk.

        Keep app_id and app_secret private.
        """

        self.app_id = app_id
        self.app_secret = app_secret
        self.ssl_verify = ssl_verify
        self.retries = retries
        self.timeout = timeout
        self.proxies = proxies

        if not endpoint:
            self._endpoint = get_config('role_login', 'api')

    def _cs_request(self, method, url, **kwargs):
        """Retry when requests.exception occurs, such as ConnectTimeout."""
        assert method.lower() in ['get', 'post', 'put', 'delete', 'head', 'options']
        attempts = 0
        backoff = random.random()
        params = kwargs.pop('params', None)
        data = kwargs.pop('data', None)
        while True:
            attempts += 1
            try:
                response = requests.request(
                    method, url, params=params, data=data, **kwargs)
                return response
            except:
                if attempts >= self.retries:
                    raise
            time.sleep(backoff)
            backoff *= 2

    def do_request(self, method, url, **kwargs):
        url = self._endpoint + url
        kwargs['verify'] = self.ssl_verify
        kwargs['timeout'] = self.timeout
        kwargs['proxies'] = self.proxies
        response = self._cs_request(method, url, **kwargs)

        try:
            body = json.loads(response.text)
        except ValueError:
            body = "Get unknown error from xyclouds:%s" % response.text
            if response.status_code >= 400:
                message = body
                raise exceptions.from_response(
                    response.status_code,
                    url, method, message)
            raise exceptions.InternalServerError(reason=body)

        return body

    def _generateMd5dign(self, data):
        """Generate sign."""
        tmp = [str(k) + str(data[k]) for k in sorted(data.keys())]
        string = self.app_secret + ''.join(tmp) + self.app_secret
        return md5.md5(string).hexdigest().upper()

    def generate_nonce(self, size=None):
        """Generate random string."""
        chars = string.ascii_letters + string.digits
        size = random.randint(1, 32) if not size else size
        return ''.join(random.choice(chars) for _ in range(size))

    def _generate_data(self):
        data = {
            'app_id': self.app_id,
            'format': 'json',
            'nonce': self.generate_nonce(),
            'sign_method': 'md5',
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        return data

    def _action(self, method, url, info):
        data = self._generate_data()
        data.update(info)
        data['sign'] = self._generateMd5dign(data)
        if method.lower() == 'get':
            kwargs = {'params': data}
        else:
            kwargs = {'json': data}
        result = self.do_request(method, url, **kwargs)
        return result

    def create_user(self, name, password, phone=None, **kwargs):
        method = 'POST'
        url = 'api/customer'
        valid_keys = ['method', 'url', 'name', 'password', 'phone']
        info = filter_out_none(locals(), valid_keys)
        info.update(kwargs)
        return self._action(method, url, info)

    def update_user(self, uuid, name=None, password=None, phone=None, **kwargs):
        """
        Edit user.
        :return: data: []
        """
        method = 'POST'
        url = 'api/customer/%s' % uuid
        valid_keys = ['method', 'url', 'name', 'password', 'phone']
        info = filter_out_none(locals(), valid_keys)
        info.update(kwargs)
        return self._action(method, url, info)

    def show_user(self, uuid):
        method = 'GET'
        url = 'api/customer/%s' % uuid
        valid_keys = ['method', 'url']
        info = filter_out_none(locals(), valid_keys)
        return self._action(method, url, info)

    def show_acmp_regions(self):
        method = 'GET'
        url = 'api/acmp/regions'
        valid_keys = ['method', 'url']
        info = filter_out_none(locals(), valid_keys)
        return self._action(method, url, info)

    def update_region_config(self):
        data = get_data(self.show_acmp_regions())
        regions = {}
        for item in data:
            regions[item['console_region']] = item['url']
        update_config('region_url', regions)

    def login(self, name, password):
        method = 'POST'
        url = 'api/login'
        valid_keys = ['method', 'url', 'name', 'password']
        info = filter_out_none(locals(), valid_keys)
        return self._action(method, url, info)
