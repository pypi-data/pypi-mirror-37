#!-*- coding:utf8 -*-
import weakref
from xycloudsclient.exceptions import ParamsInitError


class HostManager(object):
    def __init__(self, client):
        self.conn = weakref.proxy(client)
        self.url = 'host'

    def describe_host(self,
                      sort='name',
                      order='asc',
                      start=0,
                      limit=20):
        params = {
            'action': 'host__list',
            'sort': sort,
            'order': order,
            'start': start,
            'limit': limit,
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def describe_images(self):
        params = {
            'action': 'host__getimages',
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def create_host(self,
                    name,
                    desc,
                    confirm_password,
                    image_id,
                    net,
                    data_disk=None,
                    cpu=2,
                    memory=4,
                    sys_disk=50,
                    sys_volume_type='high-speed',
                    num=1):
        """创建云主机

        关于net：要求Dict格式，示例
        net = {
              "netId": "ffc83a0a-8cc3-4bfc-9141-2248958e435c",
              "net": [
                {
                  "id": "ffc83a0a-8cc3-4bfc-9141-2248958e435c",
                  "name": "子网1",
                  "ip": "192.168.0.0/24"
                }
              ],
              # 如申请公网ip
              'bandwidth': 5242880 # 公网带宽，单位byte
              "chargeType":"bandwidth",
              "lineType":"CNBGP",
              "lineName":"BGP"
            }

        关于data_disk: 要求Dict格式，示例
        data_disk = [{
                        "volume_type": "high-speed",
                        "disk_size": 50
                        "delete_on_termination": "delete"
                      }]
        关于delete_on_termination:选填项
        确定删除云主机的同时删除该数据盘
        如需删除，请确定值：'delete'

        :param name:              云主机名称
        :param desc:              云主机描述
        :param confirm_password:  云主机登录密码
        :param image_id:          镜像id
        :param net:               网络相关配置
        :param data_disk:         硬盘相关配置
        :param cpu:               cpu核心数，int类型
        :param memory:            内存大小，int类型,单位GB
        :param sys_disk:          系统盘大小，int类型,单位GB
        :param sys_volume_type:   默认'high-speed', 可选'ultra-speed'.
        :param num:               创建云主机的数量
        """
        data = {
            'action': 'host__createhost',
            'name': name,
            'desc': desc,
            'confirm_password': confirm_password,
            'image_id': image_id,
            'net': net,
            'cpu': cpu,
            'memory': memory,
            'sys_disk': sys_disk,
            'data_disk': data_disk,
            'sys_volume_type': sys_volume_type,
            'num': num,
        }
        to_json = ["net", "data_disk"]
        result = self.conn.do_request('POST', self.url,
                                      data=data, to_json=to_json)
        return result

    def open_host(self, object_ids, object_names=None):
        """
        :param object_ids:    待开机云主机id，可批量操作
        :type  object_ids:    str or list
        :param object_names:  选填，用于审计
        :type  object_names:  str or list
        """
        data = {
            'action': 'host__start',
            'object_ids': object_ids,
            'object_names': object_names,
        }
        to_str = ["object_ids", "object_names"]
        result = self.conn.do_request('POST', self.url,
                                      data=data, to_str=to_str)
        return result

    def close_host(self, object_ids, object_names=None):
        """同上"""
        data = {
            'action': 'host__stop',
            'object_ids': object_ids,
            'object_names': object_names,
        }
        to_str = ["object_ids", "object_names"]
        result = self.conn.do_request('POST', self.url, data=data,
                                      to_str=to_str)
        return result

    def close_host_force(self, object_ids, object_names=None):
        """强制关闭云主机，同上"""
        data = {
            'action': 'host__force_stop',
            'object_ids': object_ids,
            'object_names': object_names,
        }
        to_str = ["object_ids", "object_names"]
        result = self.conn.do_request('POST', self.url,
                                      data=data, to_str=to_str)
        return result

    def reboot_host(self, object_ids, object_names=None):
        """同上"""
        data = {
            'action': 'host__reboot',
            'object_ids': object_ids,
            'object_names': object_names,
        }
        to_str = ["object_ids", "object_names"]
        result = self.conn.do_request('POST', self.url,
                                      data=data, to_str=to_str)
        return result

    def delete_host(self, object_ids, object_names=None):
        """同上"""
        data = {
            'action': 'host__delete',
            'object_ids': object_ids,
            'object_names': object_names,
        }
        to_str = ["object_ids", "object_names"]
        result = self.conn.do_request('POST', self.url,
                                      data=data, to_str=to_str)
        return result

    def edit_host(self, object_ids, name, cpu, memory, desc=None):
        """编辑云主机. 只有已关机的云主机才能修改cpu和内存的数据"""
        data = {
            'action': 'host__edit',
            'name': name,
            'object_ids': object_ids,
            'cpu': cpu,
            'memory': memory,
            'desc': desc,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def get_disks(self, object_ids):
        """获取挂载在云主机的硬盘信息 """
        params = {
            'action': 'host__getinstdisks',
            'object_ids': object_ids,
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def mount_disk(self, object_ids, object_names, disk_ids):
        """挂载云硬盘
        :param object_ids: instance id
        :param object_names: instance name
        :param disk_ids: disk ids, split by ',', include those has mounted to instance
        :return:
        """
        data = {
            'action': 'host__mountdisk',
            'object_ids': object_ids,
            'object_names': object_names,
            'disk_ids': disk_ids,
        }
        to_str = ['disk_ids']
        result = self.conn.do_request('POST', self.url,
                                      data=data, to_str=to_str)
        return result

    def unmount_disk(self, object_ids, object_names, disk_ids):
        data = {
            'action': 'host__umountdisk',
            'object_ids': object_ids,
            'object_names': object_names,
            'disk_ids': disk_ids,
        }
        to_str = ['disk_ids']
        result = self.conn.do_request('POST', self.url,
                                      data=data, to_str=to_str)
        return result

    def get_net_ports(self, object_ids):
        """返回云主机公网和子网的ip和公网带宽"""
        params = {
            'action': 'host__getnetports',
            'object_ids': object_ids,
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def get_networks(self, instance_id):
        """返回云主机公网和子网的id和mac addr等信息"""
        params = {
            'action': 'host__getnetworks',
            'instance_id': instance_id,
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def get_floatips(self, object_ids):
        """获取可用的公网ip，用于给云主机配置公网ip"""
        params = {
            'action': 'host__getfloatips',
            'object_ids': object_ids,
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def get_hostips(self, dev_type='all'):
        """Get fixip for all dev, include das, db, vad, vpn, vm."""
        params = {
            'action': 'host__gethostips',
            'dev_type': dev_type,
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def get_net_list(self, object_ids):
        """获取云主机网段信息"""
        params = {
            'action': 'host__getnetlist',
            'object_ids': object_ids,
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def associate_fip(self, object_ids, object_names, current_bindips):
        """绑定或解绑公网ip

        关于current_bindips:
        [{
            "floatipid":"xxx",
            "floatip":"100.81.104.189",
            "portip":"192.168.0.33"
            }]
        如果需要解绑公网ip，将floatipid与floatip两个字段设为空

        :param object_ids:      云主机id
        :param object_names:    云主机名称
        :param current_bindips: 云主机绑定的网络信息
        :type  current_bindips: list with dict
        """
        data = {
            'action': 'host__associateip',
            'object_ids': object_ids,
            'object_names': object_names,
            'current_bindips': current_bindips,
        }
        to_json = ['current_bindips']
        result = self.conn.do_request('POST', self.url,
                                      data=data, to_json=to_json)
        return result

    def associate_subnet(self, object_ids, object_names, net_ids, mac_addr,
                         access_net=None, fixed_ip=None):
        """更新云主机子网信息，包括子网网段，ip地址，mac地址

        :param object_ids:   云主机id
        :param object_names: 云主机名称
        :param net_ids:      根据self.get_networks()获取
        :param mac_addr:     修改mac地址
        :param access_net:   网段，根据self.get_net_list()获取，或新建
        :param fixed_ip:     修改子网ip地址
        """
        data = {
            'action': 'host__connectnet',
            'object_ids': object_ids,
            'object_names': object_names,
            'net_ids': net_ids,
            'mac_addr': mac_addr,
            'access_net': access_net,
            'fixed_ip': fixed_ip,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result


class HostDetailManager(object):
    def __init__(self, client):
        self.conn = weakref.proxy(client)
        self.url = 'host/host_detail/'

    def check_host_id(self, host_id):
        if not host_id or not isinstance(host_id, basestring):
            msg = 'host_id must be string and not empty.'
            raise ParamsInitError(reason=msg)

    def host_detail_config(self, host_id):
        """返回云主机详细信息，包括磁盘、内存、网络等信息，常用磁盘使用率和内存大小"""
        self.check_host_id(host_id)
        params = {
            'action': 'host__gethostdetailcfg',
            'object_ids': host_id,
        }
        url = self.url + host_id
        result = self.conn.do_request('GET', url, params=params)
        return result

    def cpu_utilization(self, host_id, trend_cpu=6):
        """cpu使用率，默认过去六小时

        :param trend_cpu: 返回过去时间间隔的cpu使用率，单位小时，
                          默认值6,可选择24, 7*24, 15*24
        """
        self.check_host_id(host_id)
        params = {
            'action': 'host__gethosttrends',
            'object_ids': host_id,
            'trend_cpu': trend_cpu,
        }
        url = self.url + host_id
        result = self.conn.do_request('GET', url, params=params)
        return result

    def memory_utilization(self, host_id, trend_mem=6):
        """内存使用率，默认过去六小时"""
        self.check_host_id(host_id)
        params = {
            'action': 'host__gethosttrends',
            'object_ids': host_id,
            'trend_mem': trend_mem,
        }
        url = self.url + host_id
        result = self.conn.do_request('GET', url, params=params)
        return result

    def disk_io_count(self, disk_id, host_id, trend_disk_io_count=6):
        """磁盘io数，默认过去六小时"""
        self.check_host_id(host_id)
        params = {
            'action': 'host__gethosttrends',
            'object_ids': host_id,
            'disk_id': disk_id,
            'trend_disk_io_count': trend_disk_io_count,
        }
        url = self.url + host_id
        result = self.conn.do_request('GET', url, params=params)
        return result

    def disk_io_rate(self, disk_id, host_id, trend_disk_io_rate=6):
        """磁盘io速率，默认过去六小时"""
        self.check_host_id(host_id)
        params = {
            'action': 'host__gethosttrends',
            'object_ids': host_id,
            'disk_id': disk_id,
            'trend_disk_io_rate': trend_disk_io_rate,
        }
        url = self.url + host_id
        result = self.conn.do_request('GET', url, params=params)
        return result

    def internal_net_flux(self, host_id, trend_internal_net_flux=6):
        """内网流速，默认过去六小时"""
        self.check_host_id(host_id)
        params = {
            'action': 'host__gethosttrends',
            'object_ids': host_id,
            'trend_internal_net_flux': trend_internal_net_flux,
        }
        url = self.url + host_id
        result = self.conn.do_request('GET', url, params=params)
        return result

    def public_net_flux(self, object_ids='all'):
        """外网流速"""
        params = {
            'action': 'overview__getnetflux',
            'object_ids': object_ids,
        }
        result = self.conn.do_request('GET', 'overview', params=params)
        return result

    def get_vms_states(self, ids=None):
        """ 获取当前用户指定或者全部的云主机监控信息
        :param ids: 云主机id，默认值为None，请求所有主机监控信息
        :type  ids：None or list
        """
        params = {
            'action': 'overview_getvmstate',
            'ids': ids,
        }
        result = self.conn.do_request('GET', 'overview', params=params)
        return result

    def get_host_console(self, host_id):
        """获取云主机控制台地址"""
        self.check_host_id(host_id)
        params = {
            'action': 'host__getvncconsole',
            'object_ids': host_id,
        }
        url = self.url + host_id
        result = self.conn.do_request('GET', url, params=params)
        return result

