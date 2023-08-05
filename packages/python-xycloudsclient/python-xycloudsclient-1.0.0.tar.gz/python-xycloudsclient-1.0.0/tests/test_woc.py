#!-*- coding:utf-8 -*-
import string
import random
import time
import unittest
from tests.common import api_client
from tests.common import get_data
from tests.common import wait_for_server_status


def gen_random_str():
    desc_str = string.ascii_letters + string.digits + '      '
    desc = random.sample(desc_str, random.randint(1, len(desc_str)))
    return ''.join(desc)


def wait_for_woc_status(client):
    time.sleep(5)
    while True:
        woc = get_data(client.woc.get_woc())
        if not woc:
            break
        if woc['real_state'] in ['ok', 'error']:
            break
        time.sleep(5)
    return woc

def wait_woc_status(status="ACTIVE"):
    def decorator(defx):
        def wrap(self):
            res = defx(self)
            woc_info = api_client.woc.get_woc()
            instance_id = woc_info['data']['instance_id']
            wait_for_server_status(api_client, instance_id, status=status)
            return res
        return wrap
    return decorator

def ensure_woc_ok(defx):
    def wrap(self):
        ret = get_data(api_client.woc.get_woc())
        if ret['real_state'] not in ['ok', 'error']:
            wait_for_woc_status(api_client)
        return defx(self)
    return wrap

class TestWoc(unittest.TestCase):
    """test woc.WocManager"""

    def get_woc_level(self):
        ret = api_client.woc.get_woc_performance()
        level = [l['level'] for l in get_data(ret)]
        return level

    def test_get_woc(self):
        ret = api_client.woc.get_woc()
        self.assertEqual(ret['success'], 1)
        self.assertIsNotNone(ret['data'])

    def test_get_woc_performance(self):
        ret = api_client.woc.get_woc_performance()
        self.assertEqual(ret['success'], 1)
        self.assertEqual(ret['total'], 4)

    @ensure_woc_ok
    def test_get_woc_console(self):
        woc_info = api_client.woc.get_woc()
        woc_id = woc_info['data']['id']
        ret = api_client.woc.get_woc_console(woc_id)
        self.assertEqual(ret['success'], 1)
        self.assertIsNotNone(ret['data'])

    def test_create_woc(self):
        # language
        lang = random.choice(['en_US', 'zh_CN'])
        # level
        woc_level = random.choice(self.get_woc_level())
        # subnet
        subnets = api_client.network.describe_subnet_list()
        nets = [(n['id'], n['name']) for n in subnets['data']]
        net = random.choice(nets) if nets else None
        net_id = net[0] if net else None
        net_name = net[1] if net else None
        # fip
        fips = api_client.network.describe_fips()
        fips = [(i['id'], i['ip']) for i in fips['data'] if not i['bind_objid']]
        fip = random.choice(fips) if fips else None
        float_ip_id = fip[0] if fip else None
        float_ip = fip[1] if fip else None
        # desc
        desc = gen_random_str()
        # create woc
        ret = api_client.woc.create_woc(woc_level, net_id, net_name=net_name,
                                        float_ip_id=float_ip_id,
                                        float_ip=float_ip,
                                        language=lang, desc=desc)
        self.assertEqual(ret['success'], 1)
        self.assertEqual(ret['data']['conf']['level'], woc_level)
        self.assertEqual(ret['data']['language'], lang)
        self.assertEqual(ret['data']['desc'], desc)

    @wait_woc_status(status="ACTIVE")
    @ensure_woc_ok
    def test_edit_woc(self):
        woc_info = api_client.woc.get_woc()
        woc_id = woc_info['data']['id']
        # level
        origin_level = woc_info['data']['conf']['level']
        level = self.get_woc_level()
        level.remove(origin_level)
        woc_level = random.choice(level)
        # fip
        origin_float_ip_id = woc_info['data'].get('float_ip_id')
        fips = api_client.network.describe_fips()
        fips = [(i['id'], i['ip']) for i in fips['data']
                if not i['bind_objid'] and i['id'] != origin_float_ip_id]
        fip = random.choice(fips) if fips else None
        float_ip_id = fip[0] if fip else None
        float_ip = fip[1] if fip else None
        # desc
        desc = gen_random_str()
        # update woc
        ret = api_client.woc.edit_woc(woc_id, level=woc_level,
                                      float_ip_id=float_ip_id,
                                      float_ip=float_ip, desc=desc)
        self.assertEqual(ret['success'], 1)
        self.assertEqual(ret['data']['conf']['level'], woc_level)
        self.assertEqual(ret['data']['task_state'], 'UPDATING')
        self.assertEqual(ret['data']['desc'], desc)

    @wait_woc_status(status='ACTIVE')
    def test_start_woc(self):
        woc_info = api_client.woc.get_woc()
        woc_id = woc_info['data']['id']
        ret = api_client.woc.start_woc(woc_id)
        self.assertEqual(ret['success'], 1)
        self.assertEqual(ret['data']['task_state'], 'UPDATING')
        self.assertEqual(ret['data']['admin_state_up'], True)

    @wait_woc_status(status='SHUTOFF')
    @ensure_woc_ok
    def test_stop_woc(self):
        woc_info = api_client.woc.get_woc()
        woc_id = woc_info['data']['id']
        ret = api_client.woc.stop_woc(woc_id)
        self.assertEqual(ret['success'], 1)
        self.assertEqual(ret['data']['task_state'], 'UPDATING')
        self.assertEqual(ret['data']['admin_state_up'], False)

    def test_delete_woc(self):
        woc_info = api_client.woc.get_woc()
        woc_id = woc_info['data']['id']
        ret = api_client.woc.delete_woc(woc_id)
        self.assertEqual(ret['success'], 1)

    @ensure_woc_ok
    def test_api_woc(self):
        woc_info = api_client.woc.get_woc()
        woc_id = woc_info['data']['id']
        uris = ['/vmp_getinfo?get=use_cpu_all',
                'vmp_getinfo?get=iplist',
                '/vmp_getinfo?get=all']
        headers = ('User-Agent: Mozilla/5.0 (X11; Linux x86_64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
                   'Chromium/66.0.3359.181 Chrome/66.0.3359.181 Safari/537.36\n '
                   'Content-Type: application/x-www-form-urlencoded; charset=UTF-8')
        for uri in uris:
            ret = api_client.woc.api_woc(woc_id, uri, method='GET', headers=headers)
            self.assertEqual(ret['success'], 1)
            self.assertEqual(ret['data']['success'], True)


# run test by order
# python -m unittest -vv \
#         tests.test_woc.TestWoc.test_create_woc \
#         tests.test_woc.TestWoc.test_get_woc \
#         tests.test_woc.TestWoc.test_get_woc_performance \
#         tests.test_woc.TestWoc.test_get_woc_console \
#         tests.test_woc.TestWoc.test_api_woc \
#         tests.test_woc.TestWoc.test_edit_woc \
#         tests.test_woc.TestWoc.test_stop_woc \
#         tests.test_woc.TestWoc.test_start_woc \
#         tests.test_woc.TestWoc.test_delete_woc