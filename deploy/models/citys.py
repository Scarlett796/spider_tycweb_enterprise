# -*- coding: utf-8 -*-

"""
------------------------------------------------
describe:
    the model of enterprise

usage:
    

base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2020/07/11"
    __mail__ = "mingliang.gao@163.com"
------------------------------------------------
"""
from sqlalchemy import (
        Column,
        String,
        Integer,
        Boolean
)
from deploy.models import base


__all__ = ("CitysModel")


class CitysModel(base.ModelBase):
    __tablename__ = 'citys'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    full_name = Column(String(100))
    parent_id = Column(Integer)
    code = Column(String(30))
    is_cg = Column(Boolean)

