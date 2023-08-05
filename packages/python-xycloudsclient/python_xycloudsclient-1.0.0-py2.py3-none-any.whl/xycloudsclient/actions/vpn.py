#!-*- coding:utf8 -*-
import weakref
from xycloudsclient.common import get_data


class VpnManager(object):
    def __init__(self, client):
        self.conn = weakref.proxy(client)
        self.url = 'vpn/ipsec'

    def get_resource_quota(self):
        """ 返回资源配额
        :return: list
        """
        params = {
            'action': 'ipsecvpn__getresourcequota',
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def get_vpn_performance(self):
        """ 返回vpn性能选择，作为add_vpn的依赖请求
        :return: list
        """
        params = {
            'action': 'ipsecvpn__getperformance',
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def get_vpn_fip(self):
        """ 返回浮动ip地址，作为add_vpn的依赖请求
        :return: list
        """
        params = {
            'action': 'ipsecvpn__getfloatip',
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def add_vpn(self, level, resources, net_id, net_name=None,
                float_ip_id=None, float_ip=None):
        """ 添加vpn服务

        依赖参数获取
        level：         client.vpn.get_vpn_performance()
        子网 net：       client.network.describe_subnet_list()
        公网 fip：       client.vpn.get_vpn_fip()

        关于resources字段:

        五个服务，'ssl_branch', 'ssl_ssl_vpn','ssl_remoteappuser',
                'ssl_emmbasicuser'， 'ssl_emmordinaryuser'
        resources = [{
            "enable": True  # True 开启， False 关闭
            "amount": 用户数或并发数，需匹配配额
            "resource": 服务名
        }]

        :param level:            vpn性能等级，一般有1,2,3,4可选择
        :param resources:        选择服务， type: list
        :param net_id:           子网id
        :param net_name:         子网名称
        :param float_ip_id:      公网id
        :param float_ip:         公网ip
        """
        data = {
            'action': 'ipsecvpn__addipsecvpn',
            'level': level,
            'resources': resources,
            'net_id': net_id,
            'net_name': net_name,
            'float_ip_id': float_ip_id,
            'float_ip': float_ip,
        }
        to_json = ['resources']
        result = self.conn.do_request('POST', self.url, data=data,
                                      to_json=to_json)
        return result

    def get_vpn(self):
        """ 返回vpn的信息。"""
        params = {
            'action': 'ipsecvpn__getipsecvpn',
        }
        result = self.conn.do_request('GET', self.url, params=params)
        vpn_info = get_data(result)
        vpn_id = vpn_info and vpn_info.get('id', None)
        if not vpn_id:
            return result
        params['id'] = vpn_id
        tmp = self.conn.do_request('GET', self.url, params=params)
        vpn_info.update(get_data(tmp))
        return result

    def edit_vpn(self, id, level=None, resources=None,
                 float_ip_id=None, float_ip=None):
        """ 编辑vpn

        :param id:               vpn id
        :param level:            vpn性能等级
        :param resources:        资源配额
        :param float_ip_id:      公网id
        :param float_ip:         公网ip
        """
        data = {
            'action': 'ipsecvpn__editipsecvpn',
            'id': id,
            'level': level,
            'resources': resources,
            'float_ip_id': float_ip_id,
            'float_ip': float_ip,
        }
        to_json = ['resources']
        result = self.conn.do_request('POST', self.url, data=data,
                                      to_json=to_json)
        return result

    def get_vpn_console(self, id):
        """ 打开vpn控制台 """
        params = {
            'action': 'ipsecvpn__getipsecvpnconsole',
            'id': id,
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def delete_vpn(self, id):
        """ 删除vpn """
        data = {
            'action': 'ipsecvpn__deleteipsecvpn',
            'id': id,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

