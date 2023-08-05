#!-*- coding:utf8 -*-
import weakref


class SecurityManager(object):
    def __init__(self, client):
        self.conn = weakref.proxy(client)
        self.url = 'security'
    
    def describe_acl(self, order='asc', start=0, limit=20):
        """返回acl策略列表"""
        params = {
            'action': 'security__getaclpolicys',
            'order': order,
            'start': start,
            'limit': limit,
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def add_acl(self, params):
        """增加acl策略

        源和目的都有三种形式: 全部IP, 指定网络, 指定IP范围

        1.全部IP
        all_ips = {
            "start": "0.0.0.0",
            "range": "",
            "end": "255.255.255.255",
            "id": "",
            "name": ""
            }
        2.指定IP范围
        given_ips = {
            "start": "192.168.5.0",
            "range": "",
            "end": "192.168.5.255",
            "id": "",
            "name": ""
            }
        3.指定网络
        result = api_client.network.describe_subnet_list()
        net = get_data(result)
        given_net = {
            "start": "",
            "range": net[0]["ranges"][0],
            "end": "",
            "id": net[0]["id"],
            "name": net[0]["name"]
            }

        关于service: ""表示所有服务，或者指定一个或多个服务
        service_list = get_data(self.describe_service())

        关于action: 1表示允许访问， 0 表示禁止访问

        params = {
                    "id": "",
                    "source": random.choice(choice_list),
                    "target": random.choice(choice_list),
                    "service": service,
                    "action": "1",
                    "desc": "sdk add acl"
                 }
        注意：source, target和params要求Dict格式

        :param params:  "id":      ""
                        "source":  源
                        "target":  目的
                        "service": 应用于全部服务或者指定服务
                        "action":  允许访问或者禁止访问
                        "desc":    acl策略描述
        """
        data = {
            'action': 'security__addaclpolicy',
            'params': params,
        }
        to_json = ['params']
        result = self.conn.do_request('POST', self.url, data=data,
                                      to_json=to_json)
        return result

    def edit_acl(self, params):
        """ 编辑acl策略

        params要求Dict格式，其中的每个字段都需要填写

        :param params: "id":     待编辑acl策略的id,
                      "source":  修改源
                      "target":  修改目的
                      "service": 修改应用于全部服务或者指定服务
                      "action":  修改允许访问或者禁止访问
                      "desc":    修改acl策略描述
        """
        data = {
            'action': 'security__editaclpolicy',
            'params': params,
        }
        to_json = ['params', 'params.source', 'params.target']
        result = self.conn.do_request('POST', self.url, data=data,
                                      to_json=to_json)
        return result

    def describe_service(self):
        params = {
            'action': 'security__getservicelist',
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def acl_detail(self, object_ids):
        params = {
            'action': 'security__getacldetail',
            'object_ids': object_ids,
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def set_acl_status(self, status, ids, object_names=None, params=None):
        """开启或关闭一个或多个acl.

        ids, object_names, params 都是list格式

        :param status:       0 关闭； 1 开启
        :param ids:          待改变状态的acl id，用于设置，可批量操作
        :param object_names: 待改变状态的acl的描述，选填，用于操作审计
        :param params:       待改变状态的acl的参数，选填，用于操作审计
        """
        data = {
            'action': 'security__setaclpolicystatus',
            'status': status,
            'ids': ids,
            'object_names': object_names,
            'params': params,
        }
        to_json = ['params', 'ids', 'object_names']
        result = self.conn.do_request('POST', self.url, data=data,
                                      to_json=to_json)
        return result

    def delete_acl(self, ids, object_names=None, params=None):
        """删除一个或多个acl

        三个参数都需先传入list

        :param ids:           一个或多个acl id，json格式
        :param object_names:  一个或多个acl 名称，用于审计，json格式
        :param params:        一个或多个acl 参数，用于审计，json格式
        """
        data = {
            'action': 'security__deleteaclpolicys',
            'ids': ids,
            'object_names': object_names,
            'params': params,
        }
        to_json = ['params', 'ids', 'object_names']
        result = self.conn.do_request('POST', self.url, data=data,
                                      to_json=to_json)
        return result

    def add_service(self, name, protocol, content):
        """自定义服务
        :param name:      服务名
        :param protocol:  协议，TCP, UDP可选
        :param content:   端口，类型：str. 格式：22,33-34,55
        """
        data = {
            'action': 'security__addservice',
            'name': name,
            'protocol': protocol,
            'content': content,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def edit_service(self, id, name, protocol, content):
        data = {
            'action': 'security__editservice',
            'id': id,
            'name': name,
            'protocol': protocol,
            'content': content,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def delete_service(self, object_ids, object_names=None):
        """ 删除自定义服务
        :param object_ids:   一个
        :param object_names: 自定义服务名
        :return:
        """
        data = {
            'action': 'security__deleteservice',
            'object_ids': object_ids,
            'object_names': object_names,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result
    
    def get_firewall_detail(self):
        params = {
            'action': 'security__getfirewallinfo'
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result
    
    def get_firewall_performance(self):
        """获取防火墙可用配置"""
        params = {
            'action': 'security__getfirewallperformance'
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def add_firewall(self, level):
        data = {
            'action': 'security__addfirewall',
            'level': level
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def update_firewall(self, level):
        data = {
            'action': 'security__editfirewall',
            'level': level
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def change_firewall_state(self, vaf_id, do_pause):
        data = {
            'action': 'security__suspendfirewall',
            'vaf_id': vaf_id,
            'do_pause': do_pause
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def get_firewall_console_url(self, vaf_id):
        data = {
            'action': 'security__getconsole',
            'vaf_id': vaf_id
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result
    
    def delete_firewall(self, vaf_id):
        data = {
            'action': 'security__deletefirewall',
            'vaf_id': vaf_id,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def get_firewall_rules(self, vaf_id):
        """获取防火墙安全规则库"""
        params = {
            'action': 'security__afrulesnewest',
            'vaf_id': vaf_id,
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result
