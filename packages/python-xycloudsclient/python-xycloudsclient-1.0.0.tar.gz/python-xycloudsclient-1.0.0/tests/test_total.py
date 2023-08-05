#!-*- coding:utf8 -*-
import json
import os
import sys
import traceback
import unittest

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
from tests.test_disk import test_host_net, test_disk
from tests.test_host import test_host
from tests.test_network import test_net, test_fip, test_dnat, test_dns, test_static_router
from tests.test_security import test_acl, TestFirewall
from tests.test_vpn import test_vpn
from tests.test_vad import TestVad

from tests.test_user import TestUser
from tests.test_alarm import TestAlarm
from tests.test_host_detail import TestHostDetail
from tests.common import clear_resource
from tests.common import api_client

"""
注意:
**此sdk模拟页面登陆，不能处理验证码等登陆的情况**
1.严格按照页面的参数来构造参数, 一些看似无用的参数, 可能是用于操作审计
2.一些的get可以加上sort, order, start, limit进行排序、分页
3.本地时间一定要准确，否则可能导致cookie超时
"""


def test_suite():
    suite = unittest.TestSuite()
    tests = [
        TestHostDetail("test_detail_config"),
        TestHostDetail("test_cpu_utilization"),
        TestHostDetail("test_memory_utilization"),
        TestHostDetail("test_disk_io_count"),
        TestHostDetail("test_disk_io_rate"),
        TestHostDetail("test_internal_net_flux"),
        TestHostDetail("test_public_net_flux"),

        TestAlarm('test_add_alarm_policy'),
        TestAlarm('test_describe_alarm'),
        TestAlarm('test_alarm_detail'),
        TestAlarm('test_set_policy_status'),
        TestAlarm('test_edit_policy'),
        TestAlarm('test_delete_policy'),

        TestVad('test_get_vad_detail'),
        TestVad('test_vad_status'),
        TestVad('test_vad_outips'),
        TestVad('test_vad_netlist'),
        TestVad('test_update_vad'),
        TestVad('test_restart_vad'),
        TestVad('test_delete_vad'),
        TestVad('test_create_vad'),

        TestFirewall('test_get_firewall_detail'),
        TestFirewall('test_get_firewall_performance'),
        TestFirewall('test_update_fierwall'),
        TestFirewall('test_change_firewall_state'),
        TestFirewall('test_get_firewall_console_url'),
        TestFirewall('test_delete_firewall'),
        TestFirewall('test_add_firewall'),
    ]
#    suite.addTests(tests)
    tests = [TestUser('test_show_regions'),
             TestUser('test_show_basic_info'),
             TestUser('test_get_sync_urls')]
    suite.addTests(tests)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


def test_scenario(cli):
    test_host(cli)
    test_host_net(cli)
    test_net(cli)
    test_fip(cli)
    test_disk(cli)
    test_acl(cli)
    test_dnat(cli)
    test_dns(cli)
    test_static_router(cli)
    test_vpn(cli)


def main():
    try:
        # test_suite()
        # test_scenario(api_client)
        suite = unittest.TestSuite()
        tests = [

        ]
        suite.addTests(tests)

        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
    except Exception:
        print 'traceback.print_exc():'
        traceback.print_exc()
        raise
    # finally:
    #     clear_resource(api_client)


if __name__ == '__main__':
    sys.exit(main())
