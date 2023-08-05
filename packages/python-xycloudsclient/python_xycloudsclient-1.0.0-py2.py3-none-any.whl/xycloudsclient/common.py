#!-*- coding:utf8 -*-
import ConfigParser
import fcntl
import json
import os
import re
import socket

from Crypto.PublicKey import RSA as rsa
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from requests.utils import unquote
from requests import adapters
from xycloudsclient import exceptions
CONFIG_PATH = os.path.dirname(os.path.realpath(__file__)) + '/config.ini'


class TCPKeepAliveAdapter(adapters.HTTPAdapter):
    """The custom adapter used to set TCP Keep-Alive on all connections."""

    # 考虑到公网下网络环境会恶劣一点，将KEEPALIVE的总时间设置为45s(私有云原来是25s）
    def init_poolmanager(self, *args, **kwargs):
        kwargs.setdefault('socket_options', [
            (socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),
            (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),
            (socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60),
            (socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 5),
            (socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 7)
        ])
        super(TCPKeepAliveAdapter, self).init_poolmanager(*args, **kwargs)


def get_config(section, field=None, path=None):
    if path is None:
        path = CONFIG_PATH
    cf = ConfigParser.ConfigParser()
    with open(path, 'rb') as configfile:
        fcntl.flock(configfile.fileno(), fcntl.LOCK_SH)
        cf.readfp(configfile)
    if field is None:
        return cf.items(section)
    return cf.get(section, field).replace("'", '').replace('"', '')


def update_config(section, data, path=None):
    if path is None:
        path = CONFIG_PATH
    cf = ConfigParser.ConfigParser()
    with open(path, 'rb') as configfile:
        fcntl.flock(configfile.fileno(), fcntl.LOCK_SH)
        cf.readfp(configfile)
    if not cf.has_section(section):
        cf.add_section(section)
    for key in data:
        cf.set(section, key, data[key])
    with open(path, 'wb') as configfile:
        fcntl.flock(configfile.fileno(), fcntl.LOCK_EX)
        cf.write(configfile)


def encrypt(password, action='password'):
    """Encrypt password or post action by rsa.

    :param action: password/post
    """
    n = long(
        'C169B623422875FE7B68EA15FEDCF4CDA5D8528E7586649AB0C75D98D46BC03443D5A6'
        '62C243B95171173583F6870D1A528B591729137FC0244F259AF5F634FF', 16)
    if action == 'post':
        n = long('D10F977E7E6BAA6E3076FABA5EC1C17C5BF97DB202BE05C16DB8ED1704CCF'
                 '4396D478C03726AAB4401AC873F53E0D5CE41000082CA3AE5209ADF0352C1'
                 '4FAE9BCB144EAFE235C457082EDF4CE0DE2874995D9781882AC3742981189'
                 'D3F91F25B58E10205640CA5A15F15A230DF667A0C524B9814DE6FEFB9C5DA'
                 '82BEA9AAAB8B', 16)
    e = long('10001', 16)
    try:
        key = rsa.construct((n, e))
        cipher = Cipher_pkcs1_v1_5.new(key)
        return cipher.encrypt(str(password)).encode('hex')
    except Exception as e:
        message = 'encrypt password failed. %s' % e
        raise exceptions.BadRequest(message=message)


def login(session, user, password, region=None, ssl_verify=True,
          proxies=None, sync=True, timeout=300):
    """User login to xyclouds portal, and sync login to data centers.
       Session will save cookies automatically.
    """
    if not user or not password:
        raise exceptions.InvalidInput(reason='user and password must be input')
    kwargs = {
        'verify': ssl_verify,
        'proxies': proxies,
        # 设置连接和读超时时间，避免登录时因网络异常而卡住
        'timeout': timeout
    }

    login_url = get_config('role_login', 'user')
    data = {'name': user, 'password': encrypt(password)}

    # 设置心跳机制，避免网络异常时，客户端长时间不释放连接
    session.mount(login_url, TCPKeepAliveAdapter())

    resp = session.get(login_url, **kwargs)
    xsrf_token = resp.cookies.get('XSRF-TOKEN', None)
    if xsrf_token:
        session.headers['X-XSRF-TOKEN'] = unquote(xsrf_token)
    resp = session.post(login_url, json=data, **kwargs)
    content = json.loads(resp.content)
    if not content.get('success', None):
        if isinstance(content.get('data'), dict) and \
                int(content.get('data').get('lock_flag', 0)):
            left_time = content.get('data').get('left_time', '-')
            mesg = exceptions.MSG_USER_LOCKED % left_time
            raise exceptions.Unauthorized(message=mesg)
        raise exceptions.Unauthorized(message=content.get('mesg'))
    session.headers.pop('X-XSRF-TOKEN', None)
    sync_login_url = content.get('data', {}).get('login', [])
    if not sync_login_url:
        raise exceptions.Unauthorized(message=content.get('mesg'))
    if not sync:
        return sync_login_url
    to_login = [field[1] for field in get_config('region_url') if len(field) > 1]
    pattern = '|'.join(to_login)
    for one in sync_login_url:
        if not re.match(pattern, one):
            continue
        resp = session.get(one, **kwargs)
        # even if resp.status_code = 200, sync login still maybe fail.
        if resp.status_code >= 400:
            raise exceptions.Unauthorized(message=exceptions.MSG_SYNC_FAIL)


def fixoptions(options, session, domain):
    """Encrypt action in POST method, and add csrftoken as a parameter."""
    if 'action' in options:
        options['action'] = encrypt(options['action'], 'post')
    options['csrfmiddlewaretoken'] = session.cookies.get('csrftoken', domain=domain)
    return options


def filter_out_none(dictionary, keys=None):
    """ Filter out items whose value is None.
        If `keys` specified, only return non-None items with matched key.
    """
    ret = dict()
    if 'action' in dictionary:
        ret['action'] = dictionary['action']
    if keys is None:
        keys = []
    for key, value in dictionary.items():
        if value is None or key not in keys:
            continue
        ret[key] = value
    return ret


def get_data(result):
    if not result.get('success', None):
        mesg = result.get('mesg', result.get('msg', None)) or ''
        raise exceptions.InternalServerError(reason=mesg)
    data = result.get('data', None)
    return data
