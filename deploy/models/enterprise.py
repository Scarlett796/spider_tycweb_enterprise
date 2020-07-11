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
        TIMESTAMP,
        Date,
        TEXT
)
from deploy.models import base


__all__ = ("EnterpriseModel")


class EnterpriseModel(base.ModelBase):
    __tablename__ = 'enterprise'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(55))
    phone = Column(String(55))
    tyt_url = Column(String(100))
    company_url = Column(String(100))
    address = Column(String(255))
    register_funds = Column(String(20))
    paidin_funds = Column(String(20))
    establish_date = Column(Date)
    status = Column(String(30))
    credit_code = Column(String(30))
    company_type = Column(String(30))
    industry = Column(String(100))
    business_term = Column(String(55))
    resume = Column(TEXT())
    business_scope = Column(TEXT())
