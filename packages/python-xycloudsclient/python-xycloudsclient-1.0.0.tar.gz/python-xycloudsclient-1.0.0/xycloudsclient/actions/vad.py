#!-*- coding:utf8 -*-
import weakref
from xycloudsclient.common import get_data


class VadManager(object):
    def __init__(self, client):
        self.conn = weakref.proxy(client)
        self.url = 'vad'

    def get_vad_detail(self):
        params = {
            'action': 'vad__detail_list'
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def get_vad_status(self):
        params = {
            'action': 'vad__applystatus'
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def get_vad_outips(self):
        params = {
            'action': 'vad__getoutips',
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def get_vad_netlist(self):
        params = {
            'action': 'vad__getnetlist',
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def create_vad(self, level, services, net_id, float_ip_id=None):
        """
        @param services: {
                          "fast-tcp":true,
                          "ssl-offload":false,
                          "http-cache":true,
                          "smart-dns":false
                         }
        """
        data = {
            'action': 'vad__create',
            'level': level,
            'services': services,
            'net_id': net_id,
            'float_ip_id': float_ip_id
        }
        to_json = ['services']
        result = self.conn.do_request('POST', self.url, data=data,
                                      to_json=to_json)
        return result 
        
    
    def update_vad(self, level, services, vad_id):
        """ 配置vad
        """
        data = {
            'action': 'vad__edit',
            'level': level,
            'services': services,
            'vad_id': vad_id
        }
        to_json = ['services']
        result = self.conn.do_request('POST', self.url, data=data,
                                      to_json=to_json)
        return result

    def restart_vad(self, vad_id):
        """重启vad"""
        data = {
            'action': 'vad__restart',
            'vad_ids': vad_id
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def delete_vad(self, vad_id):
        """删除vad"""
        data = {
            'action': 'vad__delete',
            'vad_ids': vad_id
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def get_console_url(self, vad_id):
        """获取vad控制台url"""
        data = {
            'action': 'vad__console',
            'vad_id': vad_id
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def update_vad_outip(self, float_ip_id, float_ip):
        """更新vad公网Ip"""
        vad_detail = get_data(self.get_vad_detail())
        params = self.conn.pahelper.update_vad_outip(vad_detail)
        data = {
            'action': 'vad__edit',
            'float_ip_id': float_ip_id,
            'float_ip': float_ip
        }
        data.update(params)
        result = self.conn.do_request('POST', self.url, data=data)
        return result


