#!-*- coding:utf8 -*-
import weakref


class WocManager(object):
    def __init__(self, client):
        self.conn = weakref.proxy(client)
        self.url = 'woc'

    def get_woc(self):
        """ 返回woc的信息。"""
        params = {
            'action': 'woc__get',
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def get_woc_performance(self):
        """ 返回woc性能选择，作为create_woc的依赖请求
        :return: list
        """
        params = {
            'action': 'woc__getperformance',
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def get_woc_console(self, id):
        """ 打开woc控制台 """
        params = {
            'action': 'woc__console',
            'woc_id': id,
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def create_woc(self, level, net_id, net_name=None, float_ip_id=None,
                   float_ip=None, language='zh_CN', desc=None):
        """ 添加woc服务

        依赖参数获取
        规格 level:         client.woc.get_woc_performance()
        子网 net_id:        client.network.describe_subnet_list()
        子网名称 net_name:   client.network.describe_subnet_list()
        公网 float_ip_id:   client.network.describe_fips()
        公网IP float_ip:         公网ip
        语言 language:      zh_CN or en_US
        描述 desc:            描述字段
        """
        data = {
            'action': 'woc__create',
            'level': level,
            'language': language,
            'net_id': net_id,
            'net_name': net_name,
            'float_ip_id': float_ip_id,
            'float_ip': float_ip,
            'desc': desc
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def edit_woc(self, id, level=None, float_ip_id=None, float_ip=None,
                 desc=None):
        """ 编辑woc

        :param id:               woc id
        :param level:            woc性能等级
        :param float_ip_id:      公网id
        :param float_ip:         公网ip
        :param desc:            描述字段
        """
        data = {
            'action': 'woc__edit',
            'woc_id': id,
            'level': level,
            'float_ip_id': float_ip_id,
            'float_ip': float_ip,
            'desc': desc
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def start_woc(self, id):
        """ woc 开机

        :param id:  woc id
        """
        data = {
            'action': 'woc__start',
            'woc_id': id,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def stop_woc(self, id):
        """ woc 关机

        :param id:  woc id
        """
        data = {
            'action': 'woc__stop',
            'woc_id': id,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def delete_woc(self, id):
        """ 删除woc """
        data = {
            'action': 'woc__delete',
            'woc_ids': id,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def api_woc(self, id, uri, method=None, headers=None, data=None):
        """ woc api 操作

        :param uri:         the API URI scheme.
        :param method:      {GET,POST,PUT} request method to use.
        :param headers:     Pass custom k:v header(s) to server.
                            headers delimiter with new line \\n.
        :param data:        HTTP POST/PUT data.
        """
        data = {
            'action': 'woc__api',
            'woc_id': id,
            'uri': uri,
            'method': method,
            'headers': headers,
            'data': data
        }
        to_json = ['data']
        result = self.conn.do_request('POST', self.url, data=data,
                                      to_json=to_json)
        return result
