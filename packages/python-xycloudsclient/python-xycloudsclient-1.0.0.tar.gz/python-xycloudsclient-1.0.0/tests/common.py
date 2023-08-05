#!-*- coding:utf8 -*-
import json
import random
import string
import time
import uuid

from xycloudsclient.client import XycloudsClient
from xycloudsclient.portal_api_client import XycloudsPortalApiClient
from xycloudsclient import exceptions
from tests.test_portal_api import test_user


gb = 1024 * 1024 * 1024
mb = 1024 * 1024
CREATE_USER = False

if CREATE_USER:
    app_id = '13d0437647'
    app_secret = '3ebsleoS2FUUAjk3eEjGUtkCRkIhRzRs'
    cli = XycloudsPortalApiClient(app_id, app_secret)
    user, password = test_user(cli)
else:
    user = 'xxx@sina.com'
    password = 'Admin12345@xyclouds'
proxies = {
    'http': '127.0.0.1:3001',
    'https': '127.0.0.1:3001'
}
proxies = None
api_client = XycloudsClient(region='region-18', user=user, password=password, proxies=proxies)


def get_data(result):
    if not result['success']:
        print result['mesg']
        raise exceptions.InternalServerError(reason=result['mesg'])
    data = result['data']
    return data


def generate_nonce(size=None):
    """Generate random string."""
    chars = string.ascii_letters + string.digits
    size = random.randint(0, 32) if not size else size
    return ''.join(random.choice(chars) for _ in range(size))


def wait_for_server_status(api_client, instance_id, status='ACTIVE', timeout=300):
    params = {'action': 'host__gethoststatus',
              'object_ids': instance_id}
    instance = api_client.do_request('GET', 'host', params=params)
    instance = get_data(instance)['data']
    old_status = server_status = instance['state']
    task_status = instance['task_state']
    start_time = int(time.time())
    while True:
        if status == 'BUILD' and server_status != 'UNKNOWN':
            return
        if server_status == status and not task_status:
            return
        time.sleep(5)
        instance = api_client.do_request('GET', 'host', params=params)
        instance = get_data(instance)['data']
        server_status = instance['state']
        task_status = instance['task_state']
        if server_status != old_status:
            print 'State transition "%s" ==> "%s" after %d second wait' % (
                old_status, server_status, time.time() - start_time)
        if server_status == 'ERROR':
            raise Exception('vm build error.')
        timed_out = int(time.time()) - start_time >= timeout
        if timed_out:
            raise Exception('vm build time out.')
        old_status = server_status


def wait_for_disk_status(api_client, volume_id, status='available', timeout=300):
    def get_volume_status(volume_id):
        disks = get_data(api_client.storage.describe_disk())
        old_status = None
        for one in disks:
            if one['id'] == volume_id:
                old_status = one['status']
                task_status = one['task_state']
                break
        return old_status, task_status

    old_status, task_status = get_volume_status(volume_id)
    start_time = int(time.time())
    while True:
        if old_status == status and not task_status:
            return
        time.sleep(5)
        disk_status, task_status = get_volume_status(volume_id)
        if disk_status != old_status:
            print 'State transition "%s" ==> "%s" after %d second wait' % (
                old_status, disk_status, time.time() - start_time)
        if disk_status == 'ERROR':
            raise Exception('disk build error.')
        timed_out = int(time.time()) - start_time >= timeout
        if timed_out:
            raise Exception('disk build time out.')
        old_status = disk_status


def wait_for_vpn_status(api_client):
    time.sleep(5)
    while True:
        vpn = get_data(api_client.vpn.get_vpn())
        if not vpn:
            break
        if vpn['real_state'] in ['ok', 'error']:
            break
        time.sleep(5)
    return vpn


def create_server(api_client, is_datadisk=True, is_fip=True):
    # 镜像列表
    result = api_client.host.describe_images()
    print '=== image list ==='
    print json.dumps(result, indent=4)
    image = get_data(result)['images']['linux'][0]
    # 网络列表
    result = api_client.network.describe_subnet_list()
    net = get_data(result)[0]
    print '=== net list ==='
    print json.dumps(result, indent=4)
    # 创建虚拟机
    vm_name = 'vm-%s' % uuid.uuid4().hex[:10]
    data = {
        'cpu': 1,  # 单位:核
        'memory': 1,  # 单位:GB
        'sys_disk': image['os_image_size'] / gb,  # 单位:GB
        'sys_volume_type': random.choice(['high-speed', 'ultra-speed']),
        'name': vm_name,
        'desc': 'miao shu',
        'num': 1,
        'confirm_password': 'admin123',
        'image_id': image['id'],
        'net': {
            'netId': net['id'],
            'net': [{
                "id": net['id'],
                "name": net['name'],
                "ip": net['ranges'][0]
            }]
        }  # , 'bandwidth': 5242880}),
    }
    datadisk_size = random.choice([None, 20])
    if is_datadisk and datadisk_size:  # 是否同时创建数据盘
        datadisk_type = random.choice(['high-speed', 'ultra-speed'])
        data['data_disk'] = [{
                'volume_type': datadisk_type,
                'disk_size': datadisk_size  # 单位:GB
            }]

    # 若要申请共网ip，加上bandwidth，单位为bit
    bandwidth = random.choice([None, 5])
    if is_fip and bandwidth:
        data['net']['bandwidth'] = bandwidth * 1024 * 1024  # 单位 bit
        data['net']['lineType'] = 'CNBGP'
    data['net'] = data['net']
    result = api_client.host.create_host(**data)
    instance_id = get_data(result)['id']
    print '=== create host =='
    print json.dumps(result, indent=4)
    wait_for_server_status(api_client, instance_id)
    return instance_id, vm_name


def delete_server(api_client, instance_id, vm_name):
    # 删除虚拟机
    data = {
        'object_ids': [instance_id],
        'object_names': [vm_name]
    }
    print '=== delete hosts ==='
    result = api_client.host.delete_host(**data)
    result = get_data(result)
    is_exist = True
    while is_exist:
        instances = api_client.host.describe_host()
        instances = get_data(instances)
        is_exist = False
        for one in instances:
            if one['id'] == instance_id:
                is_exist = True
    print json.dumps(instances, indent=4)


def clear_resource(api_client):
    # 删除VPN
    vpn = get_data(api_client.vpn.get_vpn())
    if vpn and vpn['id']:
        get_data(api_client.vpn.delete_vpn(vpn['id']))
        wait_for_vpn_status(api_client)
    # 删除虚拟机
    instances = get_data(api_client.host.describe_host())
    for one in instances:
        instance_id = one['id']
        vm_name = one['name']
        delete_server(api_client, instance_id, vm_name)
    # 删除云硬盘
    time.sleep(5)  # 等待系统盘删除成功
    volumes = get_data(api_client.storage.describe_disk())
    disk_ids = []
    disk_names = []
    for one in volumes:
        disk_ids.append(one['id'])
        disk_names.append(one['name'])
    data = {
        'object_ids': ','.join(disk_ids),  # 多个以, 分隔云硬盘
        'object_names': ','.join(disk_names)
    }
    print '=== delete disks ==='
    result = api_client.storage.delete_disk(**data)
    assert result['success'] == 1
    # 删除fip
    result = get_data(api_client.network.describe_fips())
    to_disassociate = [one['id'] for one in result]
    data = api_client.pahelper.disassociate_fips(result, to_disassociate)
    print '=== disassociate_fips ==='
    result = api_client.network.disassociate_fips(ips=data)
    assert result['success'] == 1

    result = get_data(api_client.network.describe_fips())
    to_delete = [one['id'] for one in result]
    ips_list = result
    print '=== release_fips ==='
    data = api_client.pahelper.release_fips(ips_list, to_delete)
    result = api_client.network.release_fips(ips=data)
    assert result['success'] == 1
