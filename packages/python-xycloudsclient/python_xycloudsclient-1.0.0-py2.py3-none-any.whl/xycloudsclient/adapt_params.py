#!-*- coding:utf-8 -*-
import json
from copy import deepcopy

from xycloudsclient.exceptions import ParamsInitError


class ParamsAdapter(object):
    def adapt(self, params, to_json=None, to_str=None, to_list_with_dict=None):
        result = deepcopy(params)
        if to_json:
            self.json_adapter(result, params, to_json)
        if to_str:
            self.str_adapter(result, params, to_str)
        if to_list_with_dict:
            self.list_with_dict_adapter(result, params, to_list_with_dict)
        return result


    def json_adapter(self, result, params, to_json):
        # 降序排序
        to_json.sort(key=lambda item: -item.count('.'))
        for item in to_json:
            self._serialize(result, params, item.split('.'))

    @staticmethod
    def _serialize(result, params, items):

        def opt(result, params, items):
            item = items.pop()
            item_value = params.get(item)
            if not item_value or type(item_value) is str:
                return
            if items:
                opt(result.get(item), item_value, items)
            else:
                result[item] = json.dumps(item_value)
        return opt(result, params, items[::-1])

    @staticmethod
    def str_adapter(result, params, to_str):
        for item in to_str:
            item_value = params.get(item)
            if not item_value:
                continue
            if type(item_value) in (str, unicode):
                result[item] = item_value
                continue
            if type(item_value) is not list:
                raise ParamsInitError(reason="list required.")
            result[item] = ','.join(item_value)

    @staticmethod
    def list_with_dict_adapter(result, params, to_list_with_dict):
        for item in to_list_with_dict:
            item_value = params.get(item)
            if type(item_value) in (str, unicode):
                result[item] = item_value
                continue
            if type(item_value) is not list:
                raise ParamsInitError(reason="list required.")
            if len(item_value) == 0:
                continue
            if type(item_value[0]) is dict:
                result[item] = json.dumps(item_value)
            if type(item_value[0]) in (str, unicode):
                _dict = [{"id": _id} for _id in item_value]
                result[item] = json.dumps(_dict)
