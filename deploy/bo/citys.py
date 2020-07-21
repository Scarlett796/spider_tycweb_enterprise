# -*- coding: utf-8 -*-

"""
------------------------------------------------
describe:
    the db interact services of enterprise

usage:
    

base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2020/07/11"
    __mail__ = "mingliang.gao@163.com"
------------------------------------------------
"""
from deploy.bo.bo_base import BOBase
from deploy.models.citys import CitysModel
from sqlalchemy import or_, func


class CitysBo(BOBase):

    def __init__(self):
        super(CitysBo, self).__init__()

    def new_mode(self):
        return CitysModel()

    def get_count(self):
        q = self.session.query(func.count(CitysModel.id)).scalar()
        return q.count()

    def get_by_id(self, id):
        if not id:
            return {}

        q = self.session.query(
            CitysModel
        )
        q = q.filter(CitysModel.id == id)
        q = q.first()
        return q if q else {}

    def get_sub_by_pid(self, pid):
        if not pid:
            return None

        q = self.session.query(
            CitysModel
        )
        q = q.filter(CitysModel.parent_id == pid)
        q = q.all()
        return q if q else None

    def get_no_sub_citys(self):
        q = self.session.query(
            CitysModel
        )
        q = q.filter(CitysModel.is_cg == True)
        q = q.all()
        return q if q else {}