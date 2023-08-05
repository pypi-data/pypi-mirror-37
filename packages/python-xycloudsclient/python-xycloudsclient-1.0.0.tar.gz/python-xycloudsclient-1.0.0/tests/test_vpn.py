#!-*- coding:utf8 -*-
import random
import json

from tests.common import get_data, wait_for_vpn_status


def test_vpn(api_client):
    """租户已开通 中配配额"""
    # 购买vpn, 配置在配额中限制
    resource_item = ['ssl_branch', 'ssl_ssl_vpn',
                     'ssl_remoteappuser', 'ssl_emmbasicuser']
    resources = get_data(api_client.vpn.get_resource_quota())
    print '=== resources ==='
    print json.dumps(resources, indent=4)
    res = []
    for one in resources:
        if one['resource'] in resource_item:
            res.append(one)
    resources = res
    performance = get_data(api_client.vpn.get_vpn_performance())
    print '=== performance ==='
    print json.dumps(performance, indent=4)
    subnet = get_data(api_client.network.describe_subnet_list())[0]

    fips = get_data(api_client.vpn.get_vpn_fip())
    print '=== fips ==='
    print json.dumps(fips, indent=4)
    level = performance[0]['level']
    data = {
        'level': 1,
        'resources': resources,
        'net_id': subnet['id'],
        'net_name': subnet['name'],
        'float_ip_id': fips[0]['id'] if fips else None,
        'float_ip': fips[0]['ip'] if fips else None
    }
    print '=== add_vpn ==='
    print data
    vpn = get_data(api_client.vpn.add_vpn(**data))
    # 查询vpn
    vpn = wait_for_vpn_status(api_client)
    print json.dumps(vpn, indent=4)
    vpn_id = vpn['id']
    # 配置vpn,  配置在配额中限制, 更新配置会重起
    for one in resources:
        if one['enable'] is True:
            one['amount'] = 0
            break
    data = {
        'id': vpn_id,
        'level': 1,
        'resources': resources
    }
    print '=== edit_vpn resources ==='
    vpn = get_data(api_client.vpn.edit_vpn(**data))
    vpn = wait_for_vpn_status(api_client)
    # 编辑公网ip
    ran_int = random.randint(0, len(fips) - 1) if fips else 0
    data = {
        'id': vpn_id,
        'float_ip_id': fips[ran_int]['id'] if fips else None,
        'float_ip': fips[ran_int]['ip'] if fips else None
    }
    print '=== edit_vpn fip ==='
    vpn = get_data(api_client.vpn.edit_vpn(**data))
    vpn = wait_for_vpn_status(api_client)
    # 提示: 当前性能支持的最大吞吐量为 xx Mbps，建议选择宽带低于该吞吐量的公网IP。
    # 打开控制台
    vpn = get_data(api_client.vpn.get_vpn_console(vpn_id))
    print '=== get_vpn_console ==='
    print vpn
    # 删除
    vpn = get_data(api_client.vpn.delete_vpn(vpn_id))
    vpn = wait_for_vpn_status(api_client)
    print '=== complete done ==='
