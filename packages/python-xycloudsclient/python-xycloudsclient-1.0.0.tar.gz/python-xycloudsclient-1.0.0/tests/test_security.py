# !-*- coding:utf8 -*-
import random
import json
import unittest
import uuid
import time

from tests.common import get_data, api_client

STATE = (u'ok', u'error')

def test_acl(api_client):
    #  添加访问策略
    # 源和目的都有三种形式: 全部IP, 指定网络, 指定IP范围
    # 添加自定义服务
    print '=== add service==='
    data = {
        'name': 'test-%s' % uuid.uuid4().hex[:10],
        'protocol': random.choice(['TCP', 'UDP']),
        'content': '23,33-44'
    }
    result = get_data(api_client.security.add_service(**data))
    print json.dumps(result, indent=4)
    service_id = result.get('service_id', None)
    # 获取acl_service_list
    print '=== acl_servicelist ==='
    service_list = get_data(api_client.security.describe_service())
    print json.dumps(service_list, indent=4)
    is_exist = False
    for one in service_list:
        if service_id == one['id']:
            is_exist = True
            break
    assert is_exist is True
    # 编辑service
    print '=== acl_editservice ==='
    data = {
        'id': service_id,
        'name': 'test-%s' % uuid.uuid4().hex[:10],
        'protocol': random.choice(['TCP', 'UDP']),
        'content': '23,33-44'
    }
    result = api_client.security.edit_service(**data)
    assert result['success'] == 1
    service_name = data['name']
    service_list = get_data(api_client.security.describe_service())
    for one in service_list:
        if service_id == one['id']:
            assert one['name'] == data['name']
            break
    all_ips = {
        "start": "0.0.0.0",
        "range": "",
        "end": "255.255.255.255",
        "id": "",
        "name": ""
    }
    given_ips = {
        "start": "192.168.5.0",
        "range": "",
        "end": "192.168.5.255",
        "id": "",
        "name": ""
    }

    result = api_client.network.describe_subnet_list()
    net = get_data(result)
    given_net = {
        "start": "",
        "range": net[0]["ranges"][0],
        "end": "",
        "id": net[0]["id"],
        "name": net[0]["name"]
    }
    choice_list = [all_ips, given_ips, given_net]
    service = random.choice(['', [service_list[random.randint(0, len(service_list) - 1)]]])
    params = {
        "id": "",
        "source": random.choice(choice_list),
        "target": random.choice(choice_list),
        "service": service,
        "action": "1",
        "desc": "sdk add acl"
    }
    print '=== add_acl ==='
    result = api_client.security.add_acl(params=params)
    print json.dumps(result, indent=4).decode("unicode-escape")

    # acl 列表
    print '=== describe_acl ==='
    result = get_data(api_client.security.describe_acl())[0]
    print json.dumps(result, indent=4)
    acl_id = result['id']
    # acl 编辑
    service = random.choice(['', [service_list[random.randint(0, len(service_list) - 1)]]])
    params = {
        "id": acl_id,
        "source": random.choice(choice_list),
        "target": random.choice(choice_list),
        "service": service,
        "action": "1",
        "desc": "sdk edit acl"
    }
    print '=== edit_acl ==='
    result = api_client.security.edit_acl(params=json.dumps(params))
    print json.dumps(result, indent=4).decode("unicode-escape")

    result = get_data(api_client.security.acl_detail(acl_id))
    assert result['desc'] == "sdk edit acl"

    result = get_data(api_client.security.describe_acl())
    # 禁用
    status = 0
    print '=== set_acl_status ==='
    ids, object_names, params = api_client.pahelper.set_acl_status(result, [acl_id])
    result = api_client.security.set_acl_status(
        status=status,
        ids=ids, object_names=object_names, params=params
    )
    assert result['success'] == 1
    # 启用
    status = 1
    result = get_data(api_client.security.describe_acl())
    ids, object_names, params = api_client.pahelper.set_acl_status(result, [acl_id])
    result = api_client.security.set_acl_status(
        status=status,
        ids=ids, object_names=object_names, params=params
    )
    assert result['success'] == 1
    # 删除
    result = get_data(api_client.security.describe_acl())
    ids, object_names, params = api_client.pahelper.set_acl_status(result, [acl_id])
    print '=== delete_acl ==='
    result = api_client.security.delete_acl(ids, object_names, params)
    assert result['success'] == 1
    print '=== delete_services ==='
    result = api_client.security.delete_service(service_id, service_name)
    assert result['success'] == 1

class TestFirewall(unittest.TestCase):
    """test security.SecurityManager"""

    def test_get_firewall_detail(self):
        ret = api_client.security.get_firewall_detail()
        self.assertEqual(ret['success'], 1)
        print json.dumps(get_data(ret), indent=4)

    def test_get_firewall_performance(self):
        ret = api_client.security.get_firewall_performance()
        self.assertEqual(ret['success'], 1)
        print json.dumps(get_data(ret), indent=4)
    
    @staticmethod
    def wait_firewall_state():
        real_state = None
        while True:
            ret = get_data(api_client.security.get_firewall_detail())
            if not ret:
                break
            real_state = ret['real_state']
            if real_state in STATE:
                break
            time.sleep(5)
        if real_state == 'ok':
            print 'firewall state is ok'
        else:
            print 'firewall state is error'
        return real_state
            
    def test_add_firewall(self):
        ret = api_client.security.add_firewall(1)
        self.assertEqual(ret['success'], 1)
        state = self.wait_firewall_state()
        self.assertIn(state, STATE)
        
    def test_update_fierwall(self):
        ret = api_client.security.update_firewall(2)
        self.assertEqual(ret['success'], 1)
        state = self.wait_firewall_state()
        self.assertIn(state, STATE)

    def test_change_firewall_state(self):
        ret = get_data(api_client.security.get_firewall_detail())
        vaf_id = ret['vaf_id']
        ret = api_client.security.change_firewall_state(vaf_id, do_pause='true')
        self.assertEqual(ret['success'], 1)

    def test_get_firewall_console_url(self):
        ret = get_data(api_client.security.get_firewall_detail())
        vaf_id = ret['vaf_id']
        ret = api_client.security.get_firewall_console_url(vaf_id)
        self.assertEqual(ret['success'], 1)
        print json.dumps(get_data(ret), indent=4)

    def test_delete_firewall(self):
        ret = get_data(api_client.security.get_firewall_detail())
        vaf_id = ret['vaf_id']
        ret = api_client.security.delete_firewall(vaf_id)
        self.assertEqual(ret['success'], 1)
        print json.dumps(get_data(ret), indent=4)

    def test_get_firewall_rules(self):
        ret = get_data(api_client.security.get_firewall_detail())
        vaf_id = ret['vaf_id']
        ret = api_client.security.get_firewall_rules(vaf_id)
        self.assertEqual(ret['success'], 1)
        print json.dumps(get_data(ret), indent=4)
