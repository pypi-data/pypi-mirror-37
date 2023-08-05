#!-*- coding:utf-8 -*-
import json
import unittest

from tests.common import api_client, get_data


class TestAlarm(unittest.TestCase):
    """ test alarm.AlarmManager """

    def test_describe_alarm(self):
        ret = api_client.alarm.describe_alarm_policy()
        print json.dumps(ret, indent=4).decode("unicode-escape")
        self.assertEqual(ret['success'], 1)
        print json.dumps(get_data(ret), indent=4)

    def test_alarm_detail(self):
        alarm_policy = api_client.alarm.describe_alarm_policy()
        alarm_list = alarm_policy['data']
        alarm_id = None
        if len(alarm_list) > 0:
            alarm_id = alarm_list[0]['id']
        ret = api_client.alarm.get_alarm_policy_detail(object_ids=alarm_id)
        self.assertEqual(ret['success'], 1)
        print json.dumps(get_data(ret), indent=4)

    def test_add_alarm_policy(self):
        """
        Alarm policy contain: cpu, memory, disk, volume
        """

        # 只包含cpu
        params = {"name": "SDK add alarm policy",
                  "description": "only cpu",
                  "type": "vm",
                  "cpu": "on", "cpu_threshold": "80", "cpu_periods": "1",
                  "notice": "email",
                  "sms_enabled": True, "email_enabled": True,
                  "cpu_enabled": True,
                  "enabled": True}
        ret = api_client.alarm.add_alarm_policy(params)
        self.assertEqual(ret['success'], 1)

        # 包含cpu, memory. 以此类推
        params = {"name": "SDK add alarm policy 2",
                  "description": "cpu and memory",
                  "type": "vm",
                  "cpu": "on", "cpu_threshold": "80", "cpu_periods": "1",
                  "memory": "on", "memory_threshold": "80", "memory_periods": "1",
                  "notice": "email",
                  "sms_enabled": False, "email_enabled": True,
                  "cpu_enabled": True, "memory_enabled": True,
                  "enabled": True}
        ret = api_client.alarm.add_alarm_policy(params)
        self.assertEqual(ret['success'], 1)

    def test_set_policy_status(self):
        """
        Enable and disable alarm policy.
        """
        alarm_policy = api_client.alarm.describe_alarm_policy()
        alarm_list = alarm_policy['data']
        id_list, name_list = [], []
        for alarm in alarm_list:
            id_list.append(alarm['id'])
            name_list.append(alarm.get('name', ''))

        # 禁用1个
        ret = api_client.alarm.set_alarm_status(object_ids=[id_list[0]],
                                                object_names=[name_list[0]],
                                                enable=0)
        self.assertEqual(ret['success'], 1)

        # 启用1个
        ret = api_client.alarm.set_alarm_status(object_ids=[id_list[0]],
                                                object_names=[name_list[0]],
                                                enable=1)
        self.assertEqual(ret['success'], 1)

        # 禁用多个
        ret = api_client.alarm.set_alarm_status(object_ids=id_list,
                                                object_names=name_list,
                                                enable=0)
        self.assertEqual(ret['success'], 1)

        # 启用多个
        ret = api_client.alarm.set_alarm_status(object_ids=id_list,
                                                object_names=name_list,
                                                enable=1)
        self.assertEqual(ret['success'], 1)

    def test_edit_policy(self):
        """
        Test update.
        """
        alarm_policy = api_client.alarm.describe_alarm_policy()
        alarm_list = alarm_policy['data']
        _to_edit_alarm = None
        for alarm in alarm_list:
            if alarm['name'].startswith('SDK'):
                _to_edit_alarm = alarm
                break
        _to_edit_alarm_id = _to_edit_alarm['id']

        # params 和 add_alarm_policy中相同, 只修改名字
        params = {"name": "SDK edit alarm policy"}
        ret = api_client.alarm.edit_alarm_policy(object_ids=_to_edit_alarm_id,
                                                 params=params)

        self.assertEqual(ret['success'], 1)

        edited_alarm = None
        alarm_policy = api_client.alarm.describe_alarm_policy()
        alarm_list = alarm_policy['data']
        for alarm in alarm_list:
            if alarm['name'] == 'SDK edit alarm policy':
                edited_alarm = alarm
                break
        self.assertIsNotNone(edited_alarm)

    def test_delete_policy(self):
        """
        Test delete
        """
        alarm_policy = api_client.alarm.describe_alarm_policy()
        alarm_list = alarm_policy['data']
        alarm_list_len = len(alarm_list)
        _to_delete_ids, _to_delete_names = [], []
        for alarm in alarm_list:
            if alarm['name'].startswith('SDK'):
                _to_delete_ids.append(alarm['id'])
                _to_delete_names.append(alarm.get('name', ''))
        _to_delete_list_len = len(_to_delete_ids)
        ret = api_client.alarm.delete_alarm_policy(object_ids=_to_delete_ids,
                                                   object_name=_to_delete_names)
        self.assertEqual(ret['success'], 1)
        alarm_policy = api_client.alarm.describe_alarm_policy()
        alarm_list = alarm_policy['data']
        now_alarm_len = len(alarm_list)
        self.assertEqual(alarm_list_len, now_alarm_len + _to_delete_list_len)

    def test_get_alarmlog(self):
        ret = api_client.alarm.get_alarm_notification()
        self.assertEqual(ret['success'], 1)

    def test_get_unread(self):
        ret = api_client.alarm.get_unread_alarms()
        self.assertEqual(ret['success'], 1)
