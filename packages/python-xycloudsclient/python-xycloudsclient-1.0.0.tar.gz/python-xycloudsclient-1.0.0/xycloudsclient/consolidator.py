#!-*- coding:utf8 -*-
import json
from collections import defaultdict


class ParamsConstructor(object):
    """Construct parameters for request.

    Most params are modified according to the return of a list action.
    And ParamsConstrutor will help caller to do that.
    """
    def filter_valid_key(self, dictionary, keys):
        ret = dict()
        for key in keys:
            ret[key] = dictionary.get(key, None)
        return ret

    def release_fips(self, ips_info, ips):
        """
        :param ips_info:
        :param ips:
        :return:
        """
        ret = []
        valid_key = ['id', 'ip', 'bind_objid', 'bind_objname', 'bind_type']
        for one in ips_info:
            if one['ip'] not in ips:
                continue
            ret.append(self.filter_valid_key(one, valid_key))
        return ret

    def disassociate_fips(self, ips_info, ids):
        """
        :param ips_info:
        :param ips:
        :return:
        """
        ret = []
        valid_key = ['id', 'ip', 'bind_objid', 'bind_objname', 'bind_type', 'type']
        for one in ips_info:
            if one['id'] not in ids:
                continue
            ret.append(self.filter_valid_key(one, valid_key))
        return ret

    def set_router_outip(self, ips_info, ids):
        ret = defaultdict(list)
        if not ids:
            return dict()
        if ids is str:
            ids = list(ids)
        for one in ips_info:
            if one['id'] == ids[0]:
                ret['ips'].insert(0, one['ip'])
                ret['netids'].insert(0, one['external_network_id'])
                ret['subnetids'].insert(0, one['external_subnet_id'])
            elif one['id'] in ids[1:]:
                ret['ips'].append(one['ip'])
                ret['netids'].append(one['external_network_id'])
                ret['subnetids'].append(one['external_subnet_id'])
        return dict(ret)

    def edit_subnet_attribute(self, subnet_info, new_name=None, new_desc=None, new_pools=None):
        """

        :param subnet_info: dict
        :param new_name:
        :param new_desc:
        :param new_ranges:
        :return:
        """
        subnet_info['object_ids'] = subnet_info.pop('id')
        subnet_info['cidr'] = subnet_info.pop('ranges')[0]
        if new_name is not None:
            subnet_info['name'] = new_name
        if new_desc is not None:
            subnet_info['desc'] = new_desc
        if new_pools is not None:
            if isinstance(subnet_info['allocation_pools'], list):
                subnet_info['allocation_pools'] = json.dumps(new_pools)
        subnet_info.pop('conn_type')
        return subnet_info

    def set_acl_status(self, acl_list, acl_ids):
        """

        :param acl_list:
        :param acl_ids:
        :return: ids, object_names, params
        """
        params = []
        object_names = []
        for one in acl_list:
            if one['id'] in acl_ids:
                params.append(one)
                object_names.append(one['desc'])
        return acl_ids, object_names, params

    @staticmethod
    def update_vad_outip(vad_detail):
        if not vad_detail:
            return dict()
        vad_detail = vad_detail[0]
        net_info = vad_detail['wan_nic'][0]
        subnet = net_info['subnet'][0]
        params = {
            'vad_id': vad_detail['id'],
            'sub_ip': subnet['fixed_ip'],
            'sub_name': subnet['name'],
            'net_id': net_info['net-id']
        }
        return params
