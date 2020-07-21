# -*- coding: utf-8 -*-

"""
------------------------------------------------
describe:
    the services of employee

usage:
    

base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2020/1/17"
    __mail__ = "mingliang.gao@163.com"
------------------------------------------------
"""
from deploy.bo.citys import CitysBo
from deploy.utils.logger import logger as LOG
from deploy.utils.utils import get_now


class CitysService(object):

    attrs = [
        'id',
        'name',
        'full_name',
        'parent_id',
        'code',
        'is_cg'
    ]

    def __init__(self):
        super(CitysService, self).__init__()
        self.citys_bo = CitysBo()


    def get_count(self):
        count = self.citys_bo.get_count()
        return count if count else 0

    def get_by_id(self, id):
        return self.citys_bo.get_by_id(id)

    def get_subids_by_pid(self, pid):
        res = self.citys_bo.get_sub_by_pid(pid)
        if not res:
            return None
        ret = list()
        for i in res:
            if not i:
                continue
            ret.append(i.id)
        else:
            return ret

    def get_subobj_by_parid(self, pid):
        return self.citys_bo.get_sub_by_pid(pid)

    def get_no_sub_citys(self):
        ret_list = list()
        _res = self.citys_bo.get_no_sub_citys()
        if _res:
            for i in _res:
                ret_list.append(i.id)
        return ret_list

    def get_pcity_by_id(self, cid):
        city_info = self.citys_bo.get_by_id(cid)
        if not city_info:
            return {}
        city_info_pid = city_info.pid
        return self.citys_bo.get_by_id(city_info_pid)