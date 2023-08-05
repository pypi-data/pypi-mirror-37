#!-*- coding:utf8 -*-
import json
import random
import time

import requests
from requests.utils import dict_from_cookiejar

from xycloudsclient import exceptions
from xycloudsclient import consolidator
from xycloudsclient.actions import host, alarm, vad
from xycloudsclient.actions import disk
from xycloudsclient.actions import network
from xycloudsclient.actions import security
from xycloudsclient.actions import user as ac_user
from xycloudsclient.actions import vpn
from xycloudsclient.actions import woc
from xycloudsclient.adapt_params import ParamsAdapter
from xycloudsclient.common import login, filter_out_none, \
    get_config, fixoptions, TCPKeepAliveAdapter


class XycloudsClient(object):
    _endpoint = None
    _url_prex = '/dashboard/'
    _session = None

    def __init__(self, user=None, password=None, endpoint=None,
                 region=None, session=None, ssl_verify=True,
                 retries=1, timeout=300, proxies=None, version="2018-5-18",
                 signature_version="1.0"):
        """With region, session will only login on region."""

        self.user = user
        self.password = password
        self._session = session
        self.ssl_verify = ssl_verify
        self.retries = retries
        self.timeout = timeout
        self.proxies = proxies  # dict: {'http': '', 'https': ''}
        self.version = version
        self.signature_version = signature_version
        self.pahelper = consolidator.ParamsConstructor()
        self.common_params = {
            "version": version,
            "seinature_version": signature_version,
        }
        self.adapter = ParamsAdapter()

        if endpoint:
            self._endpoint = endpoint
        elif region:
            self._endpoint = get_config('region_url', region)

        if not session:
            self._session = requests.Session()
            login(self._session, user, password, region,
                  ssl_verify=ssl_verify, proxies=proxies,
                  timeout=timeout)

        self.host = host.HostManager(self)
        self.host_detail = host.HostDetailManager(self)
        self.storage = disk.DiskManager(self)
        self.network = network.NetworkManager(self)
        self.vpn = vpn.VpnManager(self)
        self.security = security.SecurityManager(self)
        self.alarm = alarm.AlarmManager(self)
        self.vad = vad.VadManager(self)
        self.woc = woc.WocManager(self)

        self.account = ac_user.UserManager(self)

    def _cs_request(self, method, url, **kwargs):
        """Retry when requests.exception occurs, such as ConnectTimeout."""
        assert method.lower() in ['get', 'post', 'put', 'delete', 'head', 'options']
        attempts = 0
        backoff = random.random()
        params = kwargs.pop('params', None)
        data = kwargs.pop('data', None)

        adaption = filter_out_none(kwargs, ['to_json', 'to_str',
                                            'to_list_with_dict'])
        if adaption:
            for key in adaption.keys():
                kwargs.pop(key)
        if params:
            params = self.adapter.adapt(params, **adaption)
            params.update(self.common_params)
        elif data:
            data = self.adapter.adapt(data, **adaption)
            data.update(self.common_params)

        if method.lower() == 'post' and data:
            domain = self._endpoint.split('//')[-1]
            data = fixoptions(data, self._session, domain)
        while True:
            attempts += 1
            try:
                self._session.mount(url, TCPKeepAliveAdapter())
                response = self._session.request(
                    method, url, params=params, data=data, **kwargs)
                return response
            except:
                if attempts >= self.retries:
                    raise
            time.sleep(backoff)
            backoff *= 2

    def do_request(self, method, url, endpoint=None, url_prex=None, **kwargs):
        _endpoint = endpoint or self._endpoint
        if _endpoint is None:
            raise exceptions.InvalidInput(
                reason='endpoint or region must be input')
        _url_prex = url_prex or self._url_prex
        url = _endpoint + _url_prex + url + '/'
        kwargs['verify'] = self.ssl_verify
        kwargs['timeout'] = self.timeout
        kwargs['proxies'] = self.proxies
        response = self._cs_request(method, url, **kwargs)
        response.encoding = 'utf-8'

        try:
            # success: {u'success': 1, u'mesg': None, u'error_count': 0, u'mesg_array': None, u'total': 0, u'data': []}
            # fail: {u'success': False, u'data': {u'count': 2,u'lock_flag': 0,u'captcha_flag': 0},u'total': None,
            # u'mesg': u'\u7528\u6237\u540d\u6216\u5bc6\u7801\u9519\u8bef'}
            body = json.loads(response.text)
        except ValueError:
            body = "Get unknown error from xyclouds:%s" % response.text
            if response.status_code >= 400:
                message = body
                raise exceptions.from_response(
                    response.status_code,
                    url, method, message)
            login_url = get_config('role_login', 'user')
            login_url = login_url.split('?')[0]
            # cookies may be expired, default to 6h
            if str(response.request.url).startswith(login_url):
                raise exceptions.Unauthorized()
            raise exceptions.InternalServerError(reason=body)

        return body

    def get_cookies(self, name, domain):
        return self._session.cookies.get(name, domain=domain)

    def get_cookies_dict(self):
        cookies_obj = self._session.cookies
        cookies_dict = dict_from_cookiejar(cookies_obj)
        return cookies_dict

    def get_uuid(self):
        kwargs = {
            'endpoint': 'https://account.xyclouds.org/',
            'url_prex': 'user/',
            'verify': True,
            'proxies': self.proxies
            }
        result  = self.do_request('GET', 'account', **kwargs)
        if not result['success']:
            return None
        try:
            basic_data = result['data']['basic']
            uuid = basic_data['uuid']
        except Exception:
            return None
        return uuid

    def get_endpoint(self):
        return self._endpoint

    def get_sync_urls(self):
        session = requests.Session()
        sync_urls = login(session, self.user, self.password, None,
                          ssl_verify=self.ssl_verify, proxies=self.proxies,
                          sync=False)
        return sync_urls

    def set_endpoint(self, region):
        self._endpoint = get_config('region_url', region)
        return self._endpoint

    @staticmethod
    def check_login(user, password, ssl_verify=None, proxies=None):
        session = requests.Session()
        login(session, user, password, None,
              ssl_verify=ssl_verify, proxies=proxies,
              sync=False)
