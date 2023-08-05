#!-*- coding:utf8 -*-
import weakref


class AlarmManager(object):
    def __init__(self, client):
        self.conn = weakref.proxy(client)
        self.url = 'manage'

    def describe_alarm_policy(self,
                              sort='name',
                              order='asc',
                              start=0,
                              limit=20
                              ):
        """ 返回告警策略条款 """
        params = {
            'action': 'manage__getalarmpolicy',
            'sort': sort,
            'order': order,
            'start': start,
            'limit': limit,
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def get_alarm_policy_detail(self, object_ids):
        """ 返回告警详情 """
        params = {
            'action': 'manage__getpolicycontent',
            'object_ids': object_ids,
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def add_alarm_policy(self, params):
        """ 添加告警策略， params要求为dict格式

        现在可以针对cpu, memory, disk, volume进行告警
        下面的参数示例对四个部分都进行监控：使用率超过80%，持续1分钟

        :param params: { "name": "add_page",
                         "description": "page",
                         "type": "vm",
                         "cpu": "on", "cpu_threshold": "80","cpu_periods": "1",
                         "memory": "on", "memory_threshold": "80", "memory_periods": "1",
                         "disk": "on", "disk_threshold": "80", "disk_periods": "1",
                          "volume": "on", "volume_threshold": "80", "volume_periods": "1",
                         "notice": "email",
                         "sms_enabled": false, "email_enabled": true,
                         "cpu_enabled": true,
                         "memory_enabled": true,
                         "disk_enabled": true,
                         "volume_enabled": true,
                         "enabled": true}
        """
        data = {
            'action': 'manage__createalarmpolicy',
            'params': params,
        }
        to_json = ['params']
        result = self.conn.do_request('POST', self.url, data=data, to_json=to_json)
        return result

    def set_alarm_status(self,
                         object_ids,
                         enable,
                         object_names=None
                         ):
        """ 开启或关闭告警策略
        :param object_ids:    告警策略id
        :type  object_ids:    str or list
        :param object_names:  告警策略名称，选填
        :type  object_names:  str or list
        :param enable:        0 关闭, 1 开启
        """
        data = {
            'action': 'manage__setpolicystate',
            'object_ids': object_ids,
            'enable': enable,
            'object_names': object_names,
        }
        to_str = ['object_ids', 'object_names']
        result = self.conn.do_request('POST', self.url, data=data, to_str=to_str)
        return result

    def edit_alarm_policy(self, object_ids, params):
        """ 编辑告警策略
        :param object_ids:  告警策略id
        :param params:      同add_alarm_policy中的params，可只填写修改部分
        :return:
        """
        data = {
            'action': 'manage__editalarmpolicy',
            'object_ids': object_ids,
            'params': params,
        }
        to_json = ['params']
        result = self.conn.do_request('POST', self.url, data=data, to_json=to_json)
        return result

    def delete_alarm_policy(self, object_ids, object_name=None):
        """ 删除告警策略
        :param object_ids:  告警策略id
        :type: object_ids:  str or list
        :param object_name: 告警策略名称，选填
        """
        data = {
            'action': 'manage__delalarmpolicy',
            'object_ids': object_ids,
            'object_name': object_name,
        }
        to_str = ['object_ids', 'object_name']
        result = self.conn.do_request('POST', self.url, data=data, to_str=to_str)
        return result

    def get_alarm_notification(self, type='list', search_value=None,
                               start=0, limit=20):
        """ 告警通知 """
        params = {
            'action': 'manage__getalarmlog',
            'type': type,
            'search_value': search_value,
            'start': start,
            'limit': limit,
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def get_unread_alarms(self):
        """ 返回未读告警数量 """
        params = {
            'action': 'manage__getunreadalarms',
        }
        result = self.conn.do_request("GET", self.url, params=params)
        return result