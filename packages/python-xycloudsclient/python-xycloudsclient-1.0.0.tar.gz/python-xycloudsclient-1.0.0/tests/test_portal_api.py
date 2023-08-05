#!-*- coding:utf8 -*-
import json
import random
import sys
from xycloudsclient import exceptions
from xycloudsclient.portal_api_client import XycloudsPortalApiClient
from xycloudsclient.common import encrypt, filter_out_none, get_config


def get_data(result):
    if not result['success']:
        print result['msg']
        raise exceptions.InternalServerError(reason=result['msg'])
    data = result['data']
    return data


def login(cli, name, password):
    method = 'POST'
    url = 'api/login'
    password = encrypt(password)
    valid_keys = ['method', 'url', 'name', 'password']
    info = filter_out_none(locals(), valid_keys)
    result = cli._action(method, url, info)
    assert result['success'] is True
    assert 'name' in result['data']
    return result


def test_user(cli):
    # 创建租户
    print '==create user=='
    name = 'testcreate%s@qq.com' % str(random.randint(0, sys.maxint))[:8]
    password = 'Admin123!@#'
    phone = random.choice([None, random.randint(10000000000, 99999999999)])
    user = cli.create_user(name, password, phone)
    print json.dumps(user, indent=4)
    user = get_data(user)
    result = cli.login(name, password)
    print '==login=='
    print json.dumps(result, indent=4)
    assert result['success'] is True
    """
    {
    "msg": "\u6210\u529f", 
    "code": "200", 
    "data": {
        "is_custom": false, 
        "name": "testcreate2875703803", 
        "certificate": 2, 
        "created_at": "2018-05-07 19:31:58", 
        "activated": 1, 
        "comp_name": "", 
        "phone": 21092115066, 
        "second_auth": false, 
        "type": "member", 
        "email": "testcreate2875703803", 
        "sf_group_id": "00ded49a851a511e8a81cfefcfea58da9", 
        "uuid": "3edc12c351ea11e8a81cfefcfea58da9"
    }, 
    "success": true
    }
    """
    # 编辑租户
    print '==update user=='
    uuid = user['uuid']
    user_name = user['name'].split('@')[0] + '@sangfor.com'
    phone = random.choice([phone, random.randint(10000000000, 99999999999)])
    old_password = password
    password = random.choice([None, 'Aa1!' + cli.generate_nonce(8)])
    print user_name, password
    result = cli.update_user(uuid, user_name, password, phone)
    print json.dumps(result, indent=4)
    """{
    "msg": "\u6210\u529f", 
    "code": "200", 
    "data": [], 
    "success": true
    }"""
    assert result['success'] is True
    # 查看租户
    print '==show user=='
    user = cli.show_user(uuid)
    print json.dumps(user, indent=4)
    user = get_data(user)
    if phone:
        assert user['phone'] == str(phone)
    assert user['name'] == user_name
    """
    {
    "msg": "\u6210\u529f", 
    "code": "200", 
    "data": {
        "comp_name": "",
        "is_custom": false, 
        "uuid": "3edc12c351ea11e8a81cfefcfea58da9", 
        "certificate": 2, 
        "activated": 1, 
        "created_at": "2018-05-07 19:31:58", 
        "pid": null, 
        "regions": [
            {
                "url": "http://gd1.console.xyclouds.cc", 
                "admin_web_url": "http://region-1.int.xyclouds.cc:88", 
                "console_region": "region-15", 
                "id": "4", 
                "name": "\u5e7f\u4e1c\u4e00\u533a"
            }
        ], 
        "phone": "51727654991", 
        "forbidden": 0, 
        "login_at": "0000-00-00 00:00:00", 
        "second_auth": false, 
        "type": "member", 
        "email": "testcreate2875703803@q.com", 
        "sf_group_id": "00ded49a851a511e8a81cfefcfea58da9", 
        "name": "testcreate2875703803@q.com"
    }, 
    "success": true
    }"""
    # 查看租户管理员区域
    print '==show acmp region=='
    regions = cli.show_acmp_regions()
    print json.dumps(regions, indent=4)
    regions = get_data(regions)
    assert len(regions) >= 1
    # 更新区域配置
    print '==update region config=='
    cli.update_region_config()
    regions = get_config('region_url')
    print json.dumps(regions, indent=4)
    # 测试密码修改成功
    if password is None:
        password = old_password
    print user_name, password
    result = cli.login(user_name, password)
    print '==login=='
    print json.dumps(result, indent=4)
    assert result['success'] is True
    return user_name, password


def main():
    app_id = '13d0437647'
    app_secret = '3ebsleoS2FUUAjk3eEjGUtkCRkIhRzRs'
    cli = XycloudsPortalApiClient(app_id, app_secret)
    test_user(cli)
    return 0


if __name__ == '__main__':
    sys.exit(main())
