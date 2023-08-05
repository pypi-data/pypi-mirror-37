#!-*- coding:utf8 -*-
import weakref


class NetworkManager(object):
    def __init__(self, client):
        self.conn = weakref.proxy(client)
        self.url = 'network'

    def describe_subnet_list(self, sort='name', order='asc',
                             start=0, limit=20):
        params = {
            'action': 'network__getsubnetlist',
            'sort': sort,
            'order': order,
            'start': start,
            'limit': limit,
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def subnet_detail(self, object_ids):
        """子网ip详细信息"""
        params = {
            'action': 'network__getsubnetdetail',
            'object_ids': object_ids,
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def edit_subnet_attribute(self, name, desc, cidr,
                              object_ids, allocation_pools,
                              gateway_ip, subnet_id):
        """编辑子网参数

        需根据self.subnet_detail()获取子网信息，只能修改name, desc, allocation_pools

        allocation_pools示例:
        [{start: "192.168.0.2", end: "192.168.0.254"}]

        :param name:              子网名称
        :param desc:              子网描述
        :param cidr:              子网网段
        :param object_ids:        网络id，对应subnet_detail的id字段
        :param allocation_pools:  申请池范围，类型为list
        :param gateway_ip:        网关ip
        :param subnet_id:         子网id
        """
        data = {
            'action': 'network__editsubnet',
            'object_ids': object_ids,
            'name': name,
            'desc': desc,
            'cidr': cidr,
            'allocation_pools': allocation_pools,
            'gateway_ip': gateway_ip,
            'subnet_id': subnet_id,
        }
        to_json = ['allocation_pools']
        result = self.conn.do_request('POST', self.url, data=data,
                                      to_json=to_json)
        return result

    def allocate_subnet(self, name, desc, cidr,
                        gateway_ip, allocation_pools='all'):
        """申请子网
        :param name:             子网名称
        :param desc:             子网描述
        :param cidr:             子网网段
        :param gateway_ip:       网关ip
        :param allocation_pools: 申请池范围. 默认值'all'，
        """
        data = {
            'action': 'network__addsubnet',
            'name': name,
            'desc': desc,
            'cidr': cidr,
            'allocation_pools': allocation_pools,
            'gateway_ip': gateway_ip,
        }
        to_json = ['allocation_pools']
        result = self.conn.do_request('POST', self.url, data=data,
                                      to_json=to_json)
        return result

    def release_subnets(self, params, object_names=None):
        """释放一个或多个子网

        关于params，要求List with dict

        params = [{
            "id": "xxx",
            "subnet_id": "xxx"
        }]

        :param params: "id":        网络id，必填，对应describe_subnet_list的id
                       "subnet_id": 子网id，必填
                       "name":      子网名称，选填
                       "net_part":  子网网段，选填

        :param object_names: 子网名称
        :type  object_names: str or list
        """
        data = {
            'action': 'network__deletesubnet',
            'params': params,
            'object_names': object_names,
        }
        to_json = ['params']
        to_str = ['object_names']
        result = self.conn.do_request('POST', self.url,
                                      data=data, to_json=to_json,
                                      to_str=to_str)
        return result

    def describe_fips(self, sort='ip', order='asc',
                      start=0, limit=20, dev_type='all'):
        """获取公网ip
        :param sort:     可选ip, bandwidth, bind_type, type_name
        :param order:    可选asc, desc
        :param start:    起始索引
        :param limit:    返回限制数量
        :param dev_type: 返回公网IP绑定的dev_type类型的设备，使用默认值即可
        """
        params = {
            'action': 'network__getpubliciplist',
            'sort': sort,
            'order': order,
            'start': start,
            'limit': limit,
            'dev_type': dev_type,
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def allocate_fips(self, bandwidth=5242880, count=1, ip_type='CNBGP'):
        """申请公网ip
        :param bandwidth: 公网ip带宽，单位bps
        :param count:     公网ip个数，目前不支持批量申请，只能为1
        :param ip_type:   公网ip线路类型
        """
        data = {
            'action': 'network__applypublicip',
            'bandwidth': bandwidth,
            'count': count,
            'type': ip_type
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def release_fips(self, ips):
        """释放一个或多个公网ip

        ips，要求list格式

        1.公网ip的id组成list
        ips = ['xxx', ]

        2.完整版
        ips = [{
            "id": "xxx",
            "ip": "xxx"
            }]

        :param ips: "id": fip id，必填，用于删除
                    "ip": fip ip，选填，用于操作审计
        """
        data = {
            'action': 'network__deletepublicip',
            'ips': ips,
        }
        to_list_with_dict = ['ips']
        result = self.conn.do_request('POST', self.url, data=data,
                                      to_list_with_dict=to_list_with_dict)
        return result

    def get_publiciptype(self):
        """获取公网ip 线路类型"""
        params = {
            'action': 'network__publiciptype',
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def change_fip_bandwidth(self, id, object_names,
                             bandwidth, count=1):
        """改变公网ip带宽
        :param id:           fip id.
        :param object_names: fip address，用于操作审计.
        :param bandwidth:    公网ip带宽，单位bps
        :param count:        公网ip个数，目前不支持批量申请，只能为1
        """
        data = {
            'action': 'network__editpublicip',
            'id': id,
            'object_names': object_names,
            'bandwidth': bandwidth,
            'count': count,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def associate_fip_to_host(self, hostip,
                              outip, outipid):
        """绑定公网ip至云主机
        :param hostip: 云主机ip地址
        :param outip:  公网ip地址
        :param outipid: fip id
        """
        data = {
            'action': 'network__bindhost',
            'hostip': hostip,
            'outip': outip,
            'outipid': outipid,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def associate_fip_to_router(self, ips=None,
                                netids=None, subnetids=None):
        """绑定公网ip至路由器
        :param ips:       公网ip地址
        :param netids:    外网network id
        :param subnetids: 外网subnet id
        """
        data = {
            'action': 'network__addrouteoutip',
            'ips': ips,
            'netids': netids,
            'subnetids': subnetids,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def disassociate_fips(self, ips):
        """ 解除绑定

        ips，要求list格式

        ips = [{
            "id": "xxx",
            "ip": "xxx",
            "bind_objid": "xxx",
            "bind_objname": "xxx",
            "bind_type": "xxx",
            "type": "xxx"
            }]

        :param ips: "id":           公网对象id，必选
                    "ip":           公网ip，必选
                    "bind_objid":   绑定对象id，必选
                    "bind_objname": 绑定对象名称，必选
                    "bind_type":    绑定对象类型，必选
                    "type":         公网ip类型，必选
        """
        data = {
            'action': 'network__clearoutip',
            'ips': ips,
        }
        to_json = ['ips']
        result = self.conn.do_request('POST', self.url, data=data,
                                      to_json=to_json)
        return result

    def disassociate_fips_by_ids(self, ids):
        respon = self.describe_fips(limit=1000)
        if respon['success'] == 0:
            return respon
        fips = respon['data']
        ips = self.conn.pahelper.disassociate_fips(fips, ids)
        result = self.disassociate_fips(ips)
        return result

    def get_router_outip(self):
        """获取可用的路由器出口ip"""
        params = {
            'action': 'network__getrouteoutips',
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def set_router_outip(self,
                         ips="",
                         netids="",
                         subnetids="",
                         del_ids=""):
        """設置或删除路由器出口ip

        设置路由器出口ip
        data = {
            'ips': 'xxx',
            'netids': 'xxx',
            'subnetids': 'xxx',
        }
        self.set_router_outip(**data)

        删除路由器出口ip

        del_ids = 'xxxx,xxxx'
        self.set_router_outip(del_ids=del_ids)

        :param ips:         公网ip地址
        :param netids:      外网network id
        :param subnetids:   外网subnet id
        :param del_ids:     带删除出口ip的id，可批量删除，由','连接
        """
        data = {
            'action': 'network__setrouteoutip',
            'ips': ips,
            'netids': netids,
            'subnetids': subnetids,
            'del_ids': del_ids,
        }
        to_str = ['ips', 'netids', 'subnetids', 'del_ids']
        result = self.conn.do_request('POST', self.url, data=data,
                                      to_str=to_str)
        return result

    def set_router_outip_by_ids(self, ids="", del_ids=""):
        respon = self.describe_fips(limit=1000)
        if respon['success'] == 0:
            return respon
        data = respon['data']
        data = self.conn.pahelper.set_router_outip(data, ids)
        data.update({'del_ids': del_ids})
        result = self.set_router_outip(**data)
        return result

    def get_dns_proxy(self):
        """获取DNS服务器"""
        params = {
            'action': 'network__getdnsproxy',
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def set_dns_proxy(self, major_dns, minor_dns):
        """设置DNS服务器
        :param major_dns: 首选DNS ip地址
        :type major_dns:  str
        :param minor_dns: 备选DNS ip地址
        :type minor_dns:  str
        """
        data = {
            'action': 'network__editdnsproxy',
            'major_dns': major_dns,
            'minor_dns': minor_dns
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result


    def describe_nats(self, sort='protocol', order='asc',
                      start=0, limit=20, dev_type='all'):
        params = {
            'action': 'network__getdnatpolicy',
            'sort': sort,
            'order': order,
            'start': start,
            'limit': limit,
            'dev_type': dev_type,
        }

        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def add_nat(self, desc, srcip, srcport,
                dstip, dstport, protocol,
                hostname='', dev_type=''):
        """ 增加NAT

        :param desc:      描述
        :param srcip:     公网IP，即源IP
        :param srcport:   源端口, 1-65535
        :param dstip:     内部IP，即目的IP
        :param dstport:   目的端口, 1-65535
        :param protocol:  协议：TCP、UDP
        :param hostname:  资源名称
        :param dev_type:  设备类型
        """
        data = {
            'action': 'network__adddnatpolicy',
            'desc': desc,
            'srcip': srcip,
            'srcport': srcport,
            'dstip': dstip,
            'dstport': dstport,
            'protocol': protocol,
            'hostname': hostname,
            'dev_type': dev_type,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def edit_nat(self, id, desc, srcip, srcport,
                 dstip, dstport, protocol,
                 hostname, servername=None, dev_type='vm', **ignore):
        """编辑NAT

        :param id:          nat对象id
        :param desc:        nat对象描述
        :param srcip:       公网IP，即源IP
        :param srcport:     源端口, 1-65535
        :param dstip:       内部IP，即目的IP
        :param dstport:     目的端口, 1-65535
        :param protocol:    协议：TCP、UDP
        :param hostname:    资源名称
        :param servername:  ""
        :param dev_type:    设备类型
        """
        data = {
            'action': 'network__editdnatpolicy',
            'id': id,
            'desc': desc,
            'srcip': srcip,
            'srcport': srcport,
            'dstip': dstip,
            'dstport': dstport,
            'protocol': protocol,
            'hostname': hostname,
            'servername': servername,
            'dev_type': dev_type,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def set_nat_status(self, status, dnats):
        """开启或者关闭NAT，可批量处理

        dnats，要求list格式

        1.dnats的id组成list
        dnats = ['xxx', ]

        2.完整版
        dnats = [{
            "id": "xxx",
            "desc": "xxx",
            ...
            }]

        :param status: 0 关闭, 1 开启
        :param dnats: "id":          nat对象id，必填
                      "desc":        nat对象描述，选填
                      "srcip":       公网IP，即源IP，选填
                      "srcport":     源端口, 1-65535，选填
                      "dstip":       内部IP，即目的IP，选填
                      "dstport":     目的端口, 1-65535，选填
                      "hostname":    资源名称，选填
                      "protocol":    协议,TCP、UDP，选填
                      "servername":  "",，选填
                      "dev_type":    设备类型，选填
        """
        data = {
            'action': 'network__setdnatstatus',
            'status': status,
            'dnats': dnats,
        }
        to_list_with_dict = ['dnats']
        result = self.conn.do_request('POST', self.url, data=data,
                                      to_list_with_dict=to_list_with_dict)
        return result

    def delete_nats(self, dnats):
        """删除NAT，可批量操作，同set_nat_status参数"""
        data = {
            'action': 'network__deletednatpolicy',
            'dnats': dnats,
        }
        to_list_with_dict = ['dnats']
        result = self.conn.do_request('POST', self.url, data=data,
                                      to_list_with_dict=to_list_with_dict)
        return result

    def describe_dns(self,
                     sort='name',
                     order='asc',
                     start=0,
                     limit=20,):
        params = {
            'action': 'network__getroutedns',
            'sort': sort,
            'order': order,
            'start': start,
            'limit': limit,
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def add_dns(self, name, ip):
        data = {
            'action': 'network__addroutedns',
            'name': name,
            'ip': ip,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def delete_dns(self, object_ids, object_names, ips):
        """删除DNS
        :param object_ids:
        :param object_names:
        :param ips:
        """
        data = {
            'action': 'network__deleteroutedns',
            'object_ids': object_ids,
            'object_names': object_names,
            'ips': ips,
        }
        to_str = ['object_ids', 'object_names']
        result = self.conn.do_request('POST', self.url, data=data,
                                      to_str=to_str)
        return result

    def edit_dns(self, name, ip, object_ids):
        data = {
            'action': 'network__editroutedns',
            'object_ids': object_ids,
            'name': name,
            'ip': ip,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def describe_static_router(self,
                               sort='dst_net',
                               order='asc',
                               start=0,
                               limit=20):
        params = {
            'action': 'network__getrouteroutes',
            'sort': sort,
            'order': order,
            'start': start,
            'limit': limit,
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def add_static_router(self, add_data):
        """添加静态路由

        格式：
        目的地址：子网掩码：下一跳地址

        add_data = "192.168.0.5:255.255.255.255:192.168.0.0"

        """
        data = {
            'action': 'network__setrouteroutes',
            'add_data': add_data,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def edit_static_router(self, edit_data):
        """修改静态路由

        格式：
        修改前!修改后

        edit_data = "192.168.0.5:255.255.255.255:192.168.0.0! \
                     192.168.0.7:255.255.255.255:192.168.0.0"
        """
        data = {
            'action': 'network__setrouteroutes',
            'edit_data': edit_data,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def delete_static_router(self, delete_data):
        """删除静态路由

        delete_data = '192.168.0.7:255.255.255.255:192.168.0.0'
        """
        data = {
            'action': 'network__setrouteroutes',
            'delete_data': delete_data,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def get_router(self):
        """获取路由器id，name"""
        params = {
            'action': 'network__getroutebindip',
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result
