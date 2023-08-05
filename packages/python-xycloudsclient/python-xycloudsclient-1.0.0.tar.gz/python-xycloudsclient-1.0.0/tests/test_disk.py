#!-*- coding:utf8 -*-
import random
import json
import time
import unittest
from tests.common import generate_nonce, get_data, wait_for_disk_status, wait_for_server_status, delete_server, \
    create_server, gb


def test_disk(api_client):
    print('add_disk')
    name = 'SDK add disk ' + generate_nonce()
    desc = name
    size = random.choice([20, 50])
    volume_type = random.choice(['high-speed', 'ultra-speed'])
    # 添加云硬盘
    result = api_client.storage.add_disk(name=name, description=desc, size=size, volume_type=volume_type)
    assert result['success'] == 1
    vol_id = get_data(result)['id']
    print json.dumps(result, indent=4)
    wait_for_disk_status(api_client, vol_id)
    # 云硬盘列表
    result = get_data(api_client.storage.describe_disk())
    print json.dumps(result, indent=4)

    instance_id, vm_name = create_server(api_client, is_datadisk=False, is_fip=False)
    data = {
        'object_ids': instance_id,
        'object_names': vm_name
    }
    print '=== close host ==='
    result = api_client.host.close_host(**data)
    wait_for_server_status(api_client, instance_id, status='SHUTOFF')
    # 获取可挂载云主机
    result = get_data(api_client.storage.get_connect_host())
    print json.dumps(result, indent=4)
    # 挂载到云主机
    data = {
        'instance_id': instance_id,
        'instance_name': vm_name,
        'object_ids': vol_id,
        'object_names': name
    }
    print '=== attach host ==='
    result = api_client.storage.disk_attach_host(**data)
    assert result['success'] == 1
    wait_for_disk_status(api_client, vol_id, 'in-use')
    # 卸载云硬盘
    print '=== detach host ==='
    result = api_client.storage.disk_detach_host(**data)
    assert result['success'] == 1
    wait_for_disk_status(api_client, vol_id, 'available')
    # 扩容,已挂载云硬盘扩容,虚拟机必须为关机状态
    add_size = random.randint(0, 20)
    data = {
        'object_ids': vol_id,
        'object_names': name,
        'add_size': add_size,
        'extended_size': size + add_size
    }
    print '=== extend volume size ==='
    result = api_client.storage.extend_disk_size(**data)
    assert result['success'] == 1
    wait_for_disk_status(api_client, vol_id, 'available')
    # 编辑云硬盘
    new_name = 'edit disk ' + generate_nonce(5)
    desc = random.choice([None, new_name])
    result = api_client.storage.edit_disk(object_ids=vol_id, name=new_name, description=desc)
    assert result['success'] == 1
    # 云硬盘列表
    result = get_data(api_client.storage.describe_disk())
    print json.dumps(result, indent=4)
    for one in result:
        if one['id'] == vol_id:
            assert one['status'] == 'available'
            assert one['description'] == desc
            assert one['name'] == new_name
            assert one['volume_type'] == volume_type
            assert one['size'] == (size + add_size) * gb
            break
    # 删除云硬盘
    delete_server(api_client, instance_id, vm_name)
    # 删除云硬盘
    data = {
        'object_ids': vol_id,
        'object_names': new_name
    }
    print '=== delete disks ==='
    result = api_client.storage.delete_disk(**data)
    assert result['success'] == 1


def test_host_net(api_client):
    instance_id, vm_name = create_server(api_client, is_datadisk=False, is_fip=False)
    # 获取虚拟机的网络
    print '=== get host net ==='
    result = get_data(api_client.host.get_net_ports(instance_id))
    hostip = result[0]['portip']
    print json.dumps(result, indent=4)
    # 获取可配置的公网ip
    print '=== get available fips ==='
    result = get_data(api_client.host.get_floatips(instance_id))
    print json.dumps(result, indent=4)
    # 虚拟机绑定公网ip
    if not result:
        print '=== allocate fip ==='
        tmp = api_client.network.allocate_fips(bandwidth=5242880, count=1)
        tmp = get_data(tmp)['sf_fip_alloc']  # 要从字典中取出
        fip_id = tmp['id'][0]
        fip = tmp['external_ip']
        print json.dumps(tmp, indent=4)
    else:
        tmp = result[0]
        fip_id = tmp['ipid']
        fip = tmp['ip']
    data = {
        'object_ids': instance_id,
        'object_names': vm_name,
        'current_bindips': json.dumps([{"floatipid": fip_id, "floatip": fip, "portip": hostip}])
    }
    print '=== bind fip ==='
    result = api_client.host.associate_fip(**data)
    assert result['success'] == 1
    # 虚拟机解绑公网ip
    data = {
        'object_ids': instance_id,
        'object_names': vm_name,
        'current_bindips': json.dumps([{"floatipid": None, "floatip": None, "portip": hostip}])
    }
    print '=== unbind fip ==='
    result = api_client.host.associate_fip(**data)
    assert result['success'] == 1

    data = {
        'object_ids': instance_id,  # 多个虚拟机以, 分隔
        'object_names': vm_name  # 多个虚拟机以, 分隔
    }
    print '=== close host ==='
    result = api_client.host.close_host(**data)
    assert result['success'] == 1
    wait_for_server_status(api_client, instance_id, 'SHUTOFF')
    # 修改虚拟机内网,只能关机修改
    result = get_data(api_client.host.get_networks(instance_id))[0]
    print '=== host network ==='
    print json.dumps(result, indent=4)
    # 获取子网列表
    print '=== subnet list ==='
    subnet_list = get_data(api_client.network.describe_subnet_list())
    print json.dumps(subnet_list, indent=4)
    access_net = []
    net_ids = []
    for one in subnet_list:
        net_ids.append(one['id'])
        access_net.append(one['name'] + '(%s)' % one['ranges'][0])

    rand_int = random.randint(0, len(net_ids) - 1)
    mac_addr = result['mac_addr'].split(':')
    mac_addr[-1] = 'ff'
    data = {
        'object_ids': instance_id,
        'object_names': vm_name,
        'net_ids': net_ids[rand_int],
        'mac_addr': ':'.join(mac_addr),
        'fixed_ip': result['fixed_ip'],
        'access_net': access_net[rand_int]
    }
    print '=== host edit network ==='
    print json.dumps(data, indent=4)
    # 重新配置子网会导致云主机绑定的公网IP失效，配置子网后需重新绑定公网IP。
    result = api_client.host.associate_subnet(**data)
    assert result['success'] == 1
    time.sleep(5)
    delete_server(api_client, instance_id, vm_name)
    result = get_data(api_client.network.describe_fips())
    ips_list = result
    print '=== release_fips ==='
    data = api_client.pahelper.release_fips(ips_list, [fip])
    result = api_client.network.release_fips(ips=data)
    assert result['success'] == 1