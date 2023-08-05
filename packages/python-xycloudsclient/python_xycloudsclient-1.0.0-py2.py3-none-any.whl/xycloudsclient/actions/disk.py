#!-*- coding:utf8 -*-
import weakref


class DiskManager(object):
    def __init__(self, client):
        self.conn = weakref.proxy(client)
        self.url = 'storage'
        
    def describe_disk(self,
                      sort='name',
                      order='asc',
                      start=0,
                      limit=20):
        params = {
            'action': 'storage__getvolumes',
            'sort': sort,
            'order': order,
            'start': start,
            'limit': limit,
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def add_disk(self,
                 name,
                 description='',
                 size=50,
                 hostname='',
                 device_id='',
                 volume_type='high-speed'):
        data = {
            'action': 'storage__createvolume',
            'name': name,
            'size': size,
            'description': description,
            'hostname': hostname,
            'device_id': device_id,
            'volume_type': volume_type,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def edit_disk(self, object_ids, name, description=None):
        data = {
            'action': 'storage__updatevolume',
            'name': name,
            'object_ids': object_ids,
            'description': description,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def extend_disk_size(self,
                         object_ids,
                         object_names,
                         add_size,
                         extended_size):
        """
        :param object_ids:    硬盘id
        :param object_names:  硬盘名称
        :param add_size:      增加的空间，单位GB
        :param extended_size: 增加后的空间，单位GB
        """
        data = {
            'action': 'storage__extendsize',
            'object_names': object_names,
            'object_ids': object_ids,
            'add_size': add_size,
            'extended_size': extended_size,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def get_connect_host(self):
        """ 获取可挂载的，即已关机的云主机， """
        params = {
            'action': 'storage__getconninsts',
        }
        result = self.conn.do_request('GET', self.url, params=params)
        return result

    def disk_attach_host(self,
                         object_ids,
                         object_names,
                         instance_name,
                         instance_id):
        """ 硬盘挂载至云主机 """
        data = {
            'action': 'storage__atachinstance',
            'object_names': object_names,
            'object_ids': object_ids,
            'instance_name': instance_name,
            'instance_id': instance_id,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def disk_detach_host(self,
                         object_ids,
                         object_names,
                         instance_name,
                         instance_id):
        """ 硬盘从云主机卸载，系统盘不能卸载 """
        data = {
            'action': 'storage__detachinstance',
            'object_names': object_names,
            'object_ids': object_ids,
            'instance_name': instance_name,
            'instance_id': instance_id,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

    def delete_disk(self,
                    object_ids,
                    object_names,
                    attach_host=None,
                    deletebackup=False):
        """删除云硬盘，需确保云硬盘已从主机中卸载

        :param object_ids:   待删除硬盘id，可批量删除
        :type  object_ids:   str or list
        :param object_names: 待删除硬盘名称，可传None
        :type  object_names: str or list
        :param attach_host:  为空
        :param deletebackup: 是否删除备份，默认为False, 否则为'delete'.
        """
        data = {
            'action': 'storage__deletevolume',
            'object_names': object_names,
            'object_ids': object_ids,
            'attach_host': attach_host,
            'deletebackup': deletebackup,
        }
        result = self.conn.do_request('POST', self.url, data=data)
        return result

