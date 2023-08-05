#!-*- coding:utf-8 -*-
import json
import time
import unittest

from tests.common import api_client, get_data


STATE = (u'ok', u'error')


class TestVad(unittest.TestCase):
    """test vad.VadManager"""

    def test_get_vad_detail(self):
        ret = api_client.vad.get_vad_detail()
        self.assertEqual(ret['success'], 1)
        if not get_data(ret):
            self.test_create_vad()
        ret = api_client.vad.get_vad_detail()
        self.assertEqual(ret['success'], 1)
        print json.dumps(get_data(ret), indent=4)

    def test_vad_status(self):
        ret = api_client.vad.get_vad_status()
        self.assertEqual(ret['success'], 1)
        print json.dumps(get_data(ret), indent=4)

    def test_vad_outips(self):
        ret = api_client.vad.get_vad_outips()
        self.assertEqual(ret['success'], 1)
        print json.dumps(get_data(ret), indent=4)

    def test_vad_netlist(self):
        ret = api_client.vad.get_vad_netlist()
        self.assertEqual(ret['success'], 1)
        print json.dumps(get_data(ret), indent=4)

    def test_create_vad(self):
        services = {
                    "fast-tcp":True,
                    "ssl-offload":False,
                    "http-cache":True,
                    "smart-dns":False
                    }
        ret = get_data(api_client.vad.get_vad_netlist())
        net_info = ret[-1]
        data = {
            'level': 1,
            'services': services,
            'net_id': net_info['id'],
        }
        ret = api_client.vad.create_vad(**data)
        self.assertEqual(ret['success'], 1)
        state = self.wait_vad_state()
        self.assertIn(state, STATE)

    def test_update_vad(self):
        status = get_data(api_client.vad.get_vad_status())[0]
        self.assertEqual(status['status'], "enabled")
        ret = get_data(api_client.vad.get_vad_detail())[0]
        vad_id = ret['id']
        data = {
            'level': 2,
            'services': status['services'],
            'vad_id': vad_id
        }
        result = api_client.vad.update_vad(**data)
        self.assertEqual(result['success'], 1)
        state = self.wait_vad_state()
        self.assertIn(state, STATE)

    @staticmethod
    def wait_vad_state():
        real_state = None
        while True:
            ret = get_data(api_client.vad.get_vad_detail())[0]
            if not ret:
                break
            real_state = ret['real_state']
            if real_state in STATE:
                break
            time.sleep(5)
        if real_state == 'ok':
            print 'vad state is ok'
        else:
            print 'vad state is error'
        return real_state

    def test_restart_vad(self):
        ret = get_data(api_client.vad.get_vad_detail())[0]
        vad_id = ret['id']
        ret = api_client.vad.restart_vad(vad_id)
        self.assertEqual(ret['success'], 1)
        state = self.wait_vad_state()
        self.assertIn(state, STATE)


    def test_delete_vad(self):
        ret = get_data(api_client.vad.get_vad_detail())[0]
        vad_id = ret['id']
        ret = api_client.vad.delete_vad(vad_id)
        self.assertEqual(ret['success'], 1)

    def test_get_vad_url(self):
        ret = get_data(api_client.vad.get_vad_detail())[0]
        vad_id = ret['id']
        ret = api_client.vad.get_console_url(vad_id)
        self.assertEqual(ret['success'], 1)
        print get_data(ret)

    def test_update_vad_outip(self):
        float_ip_infos = get_data(api_client.network.describe_fips(limit=1000))
        float_ip = dict()
        for ip in float_ip_infos:
            if not ip['bind_objid']:
                float_ip['float_ip_id'] = ip['id']
                float_ip['float_ip'] = ip['ip']
        if not float_ip:
            print 'no avalaibel fip'
            ret = api_client.network.allocate_fips()
            if ret['success'] == 0:
                raise ret['mseg']
            new_ip = get_data(ret)
            float_ip['float_ip_id'] = new_ip['sf_fip_alloc']['id'][0]
            float_ip['float_ip'] = new_ip['sf_fip_alloc']['external_ip']
        
        ret = api_client.vad.update_vad_outip(**float_ip)
        self.assertEqual(ret['success'], 1)

