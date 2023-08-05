#!-*- coding:utf8 -*-
import random
import json

from tests.common import get_data, mb, generate_nonce, create_server, delete_server


def test_net(api_client):
    """/network 页面相关: 子网"""
    # 增加子网
    randnum = random.randint(70, 80)
    allocation_pools = json.dumps([{
        'start': '192.168.%s.10' % randnum,
        'end': '192.168.%s.20' % randnum,
    }])
    data = {
        'name': 'ziwang-%s' % randnum,
        'desc': '',
        'gateway_ip': '192.168.%s.1' % randnum,
        'allocation_pools': random.choice(['all', allocation_pools]),  # 可以定义段
        'cidr': '192.168.%s.0/24' % randnum
    }
    print '=== allocate_subnet ==='
    result = api_client.network.allocate_subnet(**data)
    result = get_data(result)
    network_id = result['id']
    print json.dumps(result, indent=4)
    # 子网列表
    print '=== describe_subnet_list ==='
    result = api_client.network.describe_subnet_list()
    result = get_data(result)
    print json.dumps(result, indent=4)
    # 删除子网, 被引用的子网无法删除, 可以批量删除
    result = api_client.network.subnet_detail(network_id)
    result = get_data(result)
    to_edit = result
    # 编辑子网
    new_name = 'new' + to_edit['name']
    new_desc = 'new' + to_edit['desc']
    print '=== edit_subnet_atttribute ==='
    new_pools = [{
        'start': '192.168.%s.20' % randnum,
        'end': '192.168.%s.30' % randnum,
    }]
    to_edit = api_client.pahelper.edit_subnet_attribute(
        to_edit, new_name, new_desc, new_pools)
    print(to_edit, '**********')
    result = api_client.network.edit_subnet_attribute(**to_edit)
    assert result['success'] == 1
    # 子网详情
    print '=== subnet_detail ==='
    result = api_client.network.subnet_detail(network_id)
    result = get_data(result)
    print json.dumps(result, indent=4)
    assert result['name'] == new_name
    assert result['desc'] == new_desc
    to_delete = result
    # to_delete['net_part'] = ','.join(to_delete['ranges'])
    data = {
        'params': [to_delete],
        'object_names': new_name}
    print '=== release_subnets ==='
    result = api_client.network.release_subnets(**data)
    print(result)
    print json.dumps(result, indent=4)


def test_dnat(api_client):

    # 增加dnat, 要求路由器绑定公网ip
    result = get_data(api_client.network.get_router())
    if not result['ips']:
        bandwidth = random.randint(5, 10) * mb
        result = api_client.network.allocate_fips(bandwidth=bandwidth, count=1)
        result = get_data(result)['sf_fip_alloc']  # 要从字典中取出
        fip_id = result['id'][0]
        fip = result['external_ip']

        result = get_data(api_client.network.describe_fips())
        ips_list = result
        # 绑定到路由器
        data = {}
        for one in ips_list:
            if one['id'] == fip_id:
                data['ips'] = one['ip']
                data['netids'] = one['external_network_id']
                data['subnetids'] = one['external_subnet_id']
                break
        print '=== associate_fip_to_router ==='
        result = api_client.network.associate_fip_to_router(**data)
        assert result['success'] == 1
    else:
        fip = result['ips'][0]
    # 获取虚拟设备的内网ip,包含罢赛,das, db, vad, vpn, vm
    result =get_data(api_client.host.get_hostips())
    if not result or not result.get('host', None):
        vm = create_server(api_client, is_datadisk=False, is_fip=False)
        result = get_data(api_client.host.get_hostips())
    host = result['host'][0]
    # 同一公网ip的同一网口,只能设置一个dnat
    data1 = {
        'desc': 'sdk add nat',
        'srcip': fip,
        'srcport': random.randint(1, 65535),
        'dstip': host['ip'][0],
        'dstport': random.randint(1, 65535),
        'protocol': random.choice(['TCP', 'UDP']),
        'hostname': host['name'],
        'dev_type': host['dev_type']
    }
    data2 = {
        'desc': 'sdk add nat',
        'srcip': fip,
        'srcport': random.randint(1, 65535),
        'dstip': '2.2.2.2',
        'dstport': random.randint(1, 65535),
        'protocol': random.choice(['TCP', 'UDP']),
    }
    data = random.choice([data1, data2])
    print '=== add_nat ==='
    result = api_client.network.add_nat(**data)
    assert result['success'] == 1
    # 查询dnat
    print '=== describe_nats ==='
    result = get_data(api_client.network.describe_nats())
    print json.dumps(result, indent=4)
    dnat_data = result[0]
    # 编辑dnat
    dnat_data['desc'] = 'sdk edit nat'
    print '=== edit_nat ==='
    result = api_client.network.edit_nat(**dnat_data)
    assert result['success'] == 1
    result = get_data(api_client.network.describe_nats())
    print json.dumps(result, indent=4)
    # 起禁用
    print '=== set_nat_status ==='
    result = api_client.network.set_nat_status(status=0, dnats=json.dumps([dnat_data]))
    assert result['success'] == 1
    result = api_client.network.set_nat_status(status=1, dnats=json.dumps([dnat_data]))
    assert result['success'] == 1
    # 删除dnat
    print '=== delete_nats ==='
    result = api_client.network.delete_nats(json.dumps([dnat_data]))
    assert result['success'] == 1
    result = get_data(api_client.network.describe_nats())
    print json.dumps(result, indent=4)


def test_dns(api_client):
    ids = []
    ips = []
    object_names = []
    # 查询dns
    print '=== describe dns ==='
    ret = get_data(api_client.network.describe_dns())
    print(json.dumps(ret, indent=4))
    print '=== add dns ==='
    # 添加dns
    domain = 'www.%s.com' % generate_nonce(8)
    result = api_client.network.add_dns(name=domain, ip='192.168.0.1')
    assert result['success'] == 1
    ipdomin = result['data']['ipdomain']
    ids.append(ipdomin['id'])
    ips.append(ipdomin['ip_address'])
    object_names.append(ipdomin['domain'])
    result = get_data(result)
    print(json.dumps(result, indent=4))
    dns_id = result['ipdomain']['id']
    print '=== edit dns ==='
    # 编辑dns
    result = api_client.network.edit_dns(name=domain, ip='192.168.0.2', object_ids=dns_id)
    assert result['success'] == 1
    result = get_data(api_client.network.describe_dns())
    print(json.dumps(result, indent=4))

    # 删除dns
    print '=== delete dns ==='
    result = api_client.network.delete_dns(ids, object_names, ips)
    assert result['success'] == 1


def test_fip(api_client):
    """/network/public_ip 页面相关: 公网ip"""
    # 创建公网IP
    print '=== allocate fip ==='
    bandwidth = random.randint(5, 10) * mb
    result = api_client.network.allocate_fips(bandwidth=bandwidth, count=1)
    result = get_data(result)['sf_fip_alloc'] # 要从字典中取出
    fip_id = result['id'][0]
    fip = result['external_ip']
    print json.dumps(result, indent=4)
    """{
        "subnet_type": "CNBGP",
        "external_ip": "100.91.1.3",
        "external_network_id": "0db7cc35-c752-4ada-bc69-b7c3ebcb0091",
        "created_at": "2018-04-09 09:27:56.392551",
        "qos_uplink": 640,
        "qos_downlink": 640,
        "tenant_id": "a5b6cfce373511e89703fefcfe0cf028",
        "external_subnet_id": "c25b06c2-e6cf-48f3-854e-0df7bf01e534",
        "id": ["9a49e251-35b8-47c2-bc97-f800313beddc"]
    }"""
    # 编辑公网ip
    print '=== change_fip_bandwidth ==='
    result = api_client.network.change_fip_bandwidth(
        id=fip_id,
        object_names=fip,
        bandwidth=bandwidth + 1,
        count=1
    )
    assert result['success'] == 1
    # 绑定到云主机
    instance_id, vm_name = create_server(api_client, is_datadisk=False, is_fip=False)
    result = api_client.host.get_net_ports(instance_id)
    fixip = get_data(result)[0]['portip']
    print '=== associate_fip_to_host ==='
    result = api_client.network.associate_fip_to_host(
        hostip=fixip,
        outip=fip,
        outipid=fip_id
    )
    print json.dumps(get_data(result), indent=4)

    # 解除绑定
    # 公网ip列表
    result = get_data(api_client.network.describe_fips())
    ips_list = result
    print json.dumps(result, indent=4)
    """
    [{
            "ip": "100.81.107.73",
            "bind_objid": "fab8e44a-7f94-47b1-8223-10675c91a357",
            "bind_objname": "\u5566\u5566",
            "external_network_id": "f6d65805-8aad-42de-9d28-5c10b2a1284a",
            "type_name": "BGP",
            "bandwidth": 10485760,
            "bind_objip": null,
            "bind_type": "vm",
            "external_subnet_id": "7ae42a65-3799-4c8e-8f19-3e50d456004f",
            "type": "CNBGP",
            "id": "5ab34331-a24e-481a-9bba-84729754b67f"
        }]
        """
    # to_disassociate = [fip]
    # data = api_client.pahelper.disassociate_fips(ips_list, to_disassociate)
    print '=== disassociate_fips ==='
    result = api_client.network.disassociate_fips_by_ids(fip_id)
    assert result['success'] == 1
    print json.dumps(result, indent=4)
    # 绑定到路由器
    data = {}
    for one in ips_list:
        if one['id'] == fip_id:
            data['ips'] = one['ip']
            data['netids'] = one['external_network_id']
            data['subnetids'] = one['external_subnet_id']
            break
    print '=== associate_fip_to_router ==='
    result = api_client.network.associate_fip_to_router(**data)
    assert result['success'] == 1
    router = get_data(api_client.network.get_router())
    print json.dumps(router, indent=4)
    assert fip in router['ips']
    # 解除绑定
    result = get_data(api_client.network.describe_fips())
    ips_list = result
    print '=== disassociate_fips ==='
    # data = api_client.pahelper.disassociate_fips(ips_list, to_disassociate)
    result = api_client.network.disassociate_fips_by_ids(fip_id)
    assert result['success'] == 1

    # 删除公网IP
    to_delete = [fip]
    print '=== release_fip ==='
    result = get_data(api_client.network.describe_fips())
    ips_list = result
    data = api_client.pahelper.release_fips(ips_list, to_delete)
    result = api_client.network.release_fips(ips=data)
    result = get_data(result)
    print json.dumps(result, indent=4)
    delete_server(api_client, instance_id, vm_name)

    # 获取DNS服务器信息
    result = api_client.network.get_dns_proxy()
    assert  result['success'] == 1
    result = get_data(result)
    print(json.dumps(result, indent=4))

    #设置DNS服务器ip
    old_major_dns = result['major_dns']
    old_minor_dns = result['minor_dns']

    new_minnor_dns = '1.2.4.9'
    result = api_client.network.set_dns_proxy(old_major_dns, new_minnor_dns)
    assert result['success'] == 1

    result = get_data(api_client.network.get_dns_proxy())
    now_minor_dns = result['minor_dns']
    print(json.dumps(result, indent=4))
    assert now_minor_dns == new_minnor_dns

    # 还原
    result = api_client.network.set_dns_proxy(old_major_dns, old_minor_dns)
    assert result['success'] == 1





def test_static_router(api_client):
    """"""
    # 下一跳地址 必须是一个已存在 子网的地址
    # 增加静态路由
    print('add_static_router')
    dst_net = '3.3.3.3'
    dst_mask = '255.255.255.255'
    nexthop = '192.168.0.6'
    add_data = ':'.join([dst_net, dst_mask, nexthop])
    result = api_client.network.add_static_router(add_data)
    assert result['success'] == 1
    print('describe_static_router')
    result = api_client.network.describe_static_router()
    print json.dumps(result, indent=4).decode("unicode-escape")

    static_router = get_data(result)[0]

    print('edit_dns')
    edit_data = static_router['dst_net'] + ':' + static_router['dst_mask'] + ':' + \
        static_router['nexthop'] + '!192.168.0.66'+ ':' + static_router['dst_mask'] + ':' + \
                static_router['nexthop']
    result = api_client.network.edit_static_router(edit_data)
    print json.dumps(result, indent=4).decode("unicode-escape")

    print('delete_static_router')
    result = get_data(api_client.network.describe_static_router())
    data = []
    for one in result:
        data.append('%s:%s:%s' % (one['dst_net'], one['dst_mask'], one['nexthop']))
    result = api_client.network.delete_static_router(','.join(data))
    assert result['success'] == 1
    print json.dumps(result, indent=4).decode("unicode-escape")
