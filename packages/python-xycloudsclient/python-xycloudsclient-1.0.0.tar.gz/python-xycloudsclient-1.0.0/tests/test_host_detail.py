import json
import unittest

from tests.common import api_client
from tests.common import get_data, mb, generate_nonce, create_server, delete_server


class TestHostDetail(unittest.TestCase):
    """test host.HostDetailManager"""

    @classmethod
    def setUpClass(cls):
        host_data = api_client.host.describe_host()
        hosts = host_data['data']
        if not hosts:
            create_server(api_client, is_datadisk=False, is_fip=False)
            host_data = api_client.host.describe_host()
            hosts = host_data['data']
        assert len(hosts) > 0
        cls.host_id = hosts[0]['id']
        cls.detail = api_client.host_detail

    @classmethod
    def tearDownClass(cls):
        instances = get_data(api_client.host.describe_host())
        for one in instances:
            instance_id = one['id']
            vm_name = one['name']
            delete_server(api_client, instance_id, vm_name)

    def test_detail_config(self):
        ret = self.detail.host_detail_config(self.host_id)
        self.assertEqual(ret['success'], 1)
        data = ret['data']
        print(json.dumps(data, indent=4))

    def test_cpu_utilization(self):
        ret = self.detail.cpu_utilization(self.host_id)
        self.assertEqual(ret['success'], 1)
        data = ret['data']
        print(json.dumps(data, indent=4))

    def test_memory_utilization(self):
        ret = self.detail.memory_utilization(self.host_id)
        self.assertEqual(ret['success'], 1)
        data = ret['data']
        print(json.dumps(data, indent=4))

    def test_disk_io_count(self):
        ret = self.detail.host_detail_config(self.host_id)
        self.assertEqual(ret['success'], 1)
        data = ret['data']
        disk_data = data['disk']
        sys_disk_id = disk_data[0]['id']
        ret = self.detail.disk_io_count(sys_disk_id, self.host_id)
        self.assertEqual(ret['success'], 1)
        data = ret['data']
        print(json.dumps(data, indent=4))

    def test_disk_io_rate(self):
        ret = self.detail.host_detail_config(self.host_id)
        self.assertEqual(ret['success'], 1)
        data = ret['data']
        disk_data = data['disk']
        sys_disk_id = disk_data[0]['id']
        ret = self.detail.disk_io_rate(sys_disk_id, self.host_id)
        self.assertEqual(ret['success'], 1)
        data = ret['data']
        print(json.dumps(data, indent=4))

    def test_internal_net_flux(self):
        ret = self.detail.internal_net_flux(self.host_id)
        self.assertEqual(ret['success'], 1)
        data = ret['data']
        print(json.dumps(data, indent=4))

    def test_public_net_flux(self):
        ret = self.detail.public_net_flux(self.host_id)
        self.assertEqual(ret['success'], 1)
        data = ret['data']
        print(json.dumps(data, indent=4))

    def test_get_vms_state(self):
        ret = self.detail.get_vms_states()
        self.assertEqual(ret['success'], 1)
        data = ret['data']
        print(json.dumps(data, indent=4))

    def test_get_host_console(self):
        ret = self.detail.get_host_console(self.host_id)
        self.assertEqual(ret['success'], 1)
        data = ret['data']
        print(json.dumps(data, indent=4))
