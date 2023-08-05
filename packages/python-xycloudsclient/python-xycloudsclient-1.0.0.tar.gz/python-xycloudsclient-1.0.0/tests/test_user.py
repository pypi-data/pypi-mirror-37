#!-*- coding:utf-8 -*-
import json
import unittest
from tests.common import api_client, get_data


class TestUser(unittest.TestCase):
    """ test user info from account."""

    def test_show_regions(self):
        ret = api_client.account.show_regions()
        self.assertEqual(ret['success'], 1)
        data = get_data(ret)
        print json.dumps(data, indent=4)
        region = data[0]
        self.assertIn('url', region)
        self.assertIn('id', region)
        self.assertIn('name', region)

    def test_show_basic_info(self):
        ret = api_client.account.show_basic()
        self.assertEqual(ret['success'], 1)
        data = get_data(ret)
        print json.dumps(data, indent=4)
        self.assertIn('basic', data)

    def test_get_sync_urls(self):
        ret = api_client.get_sync_urls()
        self.assertIsInstance(ret, list)
