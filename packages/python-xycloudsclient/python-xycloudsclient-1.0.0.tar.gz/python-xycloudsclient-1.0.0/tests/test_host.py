#!-*- coding:utf8 -*-
import random
import json
import time
import uuid

from tests.common import get_data, wait_for_disk_status, wait_for_server_status, delete_server, \
    create_server, gb


def test_host(api_client):
    """/host 页面相关"""
    instance_id, vm_name = create_server(api_client)
    # 虚拟机列表
    instances = get_data(api_client.host.describe_host())
    print '=== host list ==='
    print json.dumps(instances, indent=4)
    # 关闭虚拟机
    data = {
        'object_ids': instance_id,  # 多个虚拟机以, 分隔
        'object_names': vm_name  # 多个虚拟机以, 分隔
        }
    print '=== close host ==='
    result = api_client.host.close_host(**data)
    assert result['success'] == 1
    wait_for_server_status(api_client, instance_id, 'SHUTOFF')
    # 开启虚拟机
    print '=== open host ==='
    result = api_client.host.open_host(**data)
    assert result['success'] == 1
    wait_for_server_status(api_client, instance_id)
    # 重启虚拟机
    print '=== reboot host ==='
    result = api_client.host.reboot_host(**data)
    assert result['success'] == 1
    time.sleep(2)
    wait_for_server_status(api_client, instance_id)
    # 强制关机
    print '=== force close host ==='
    result = api_client.host.close_host_force(**data)
    assert result['success'] == 1
    wait_for_server_status(api_client, instance_id, 'SHUTOFF')
    # 编辑虚拟机
    vm_name = 'new' + vm_name
    new_cpu = 2
    new_mem = 4
    result = api_client.host.edit_host(instance_id, vm_name, new_cpu, new_mem)
    assert result['success'] == 1
    instances = get_data(api_client.host.describe_host())
    print json.dumps(instances, indent=4)
    for one in instances:
        if one['id'] == instance_id:
            assert one['core'] == new_cpu
            assert one['name'] == vm_name
            assert one['mem'] == new_mem * gb
            break
    # 挂载云硬盘,只有关机状态可以
    # 创建云硬盘
    name = 'SDK add disk %s' % uuid.uuid4().hex[:10]
    desc = 'xycloud sdk'
    size = random.choice([20, 50])
    volume_type = random.choice(['high-speed', 'ultra-speed'])
    print '=== create disk ==='
    result = api_client.storage.add_disk(name=name, description=desc, size=size,
                                 volume_type=volume_type)
    disk = get_data(result)
    volume_id = disk['id']
    wait_for_disk_status(api_client, volume_id)
    # 获取云主机已挂载和可挂载的云硬盘
    print '=== host get disks ==='
    result = api_client.host.get_disks(instance_id)
    print json.dumps(get_data(result), indent=4)
    unuse_disks = get_data(result)['unuse']
    unuse_disk_ids = [one['id'] for one in unuse_disks]
    assert volume_id in unuse_disk_ids
    mount_disks = [volume_id]
    use_disks = get_data(result)['used']
    for one in use_disks:
        mount_disks.append(one['id'])
    # 挂载云硬盘
    # ** 已挂载在vm上的disk,需要增加到disk_ids中，否则会被卸载 **
    data = {
        'object_ids': instance_id,
        'object_names': vm_name,
        'disk_ids': ','.join(mount_disks)
    }
    print '=== host mount disks ==='
    result = api_client.host.mount_disk(**data)
    assert result['success'] == 1
    wait_for_server_status(api_client, instance_id, 'SHUTOFF')

    result = api_client.host.get_disks(instance_id)
    used_disks = get_data(result)['used']
    disk_ids = []
    disk_names = []
    for one in used_disks:
        disk_ids.append(one['id'])
        disk_names.append(one['name'])
    # 卸载云硬盘
    data = {
        'object_ids': instance_id,
        'object_names': vm_name,
        'disk_ids': ','.join(disk_ids)
    }
    print '=== host unmount disks ==='
    result = api_client.host.unmount_disk(**data)
    assert result['success'] == 1
    wait_for_server_status(api_client, instance_id, 'SHUTOFF')
    # check
    instances = get_data(api_client.host.describe_host())
    fip = None
    for one in instances:
        if one['id'] == instance_id:
            assert len(one['disk']) == 1
            fip = one['public_ip']
            break

    delete_server(api_client, instance_id, vm_name)
    # 删除云硬盘
    data = {
        'object_ids': ','.join(disk_ids),  # 多个以, 分隔云硬盘
        'object_names': ','.join(disk_names)
    }
    print '=== delete disks ==='
    result = api_client.storage.delete_disk(**data)
    assert result['success'] == 1
    # 删除fip
    if fip:
        result = get_data(api_client.network.describe_fips())
        ips_list = result
        print '=== release_fips ==='
        data = api_client.pahelper.release_fips(ips_list, fip)
        result = api_client.network.release_fips(ips=data)
        assert result['success'] == 1
