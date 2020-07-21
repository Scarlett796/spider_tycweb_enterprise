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
from deploy.bo.enterprise import EnterpriseBo
from deploy.utils.logger import logger as LOG
from deploy.utils.utils import get_now


class EnterpriseService(object):

    attrs = [
        'id',
        'name',
        'email',
        'phone',
        'tyt_url',
        'company_url',
        'address',
        'register_funds'
        'paidin_funds',
        'establish_date',
        'status',
        'credit_code',
        'company_type',
        'industry',
        'business_term',
        'resume',
        'business_scope',
        'key',
        'city',
        'sub_city'
    ]

    def __init__(self):
        super(EnterpriseService, self).__init__()
        self.enterprise_bo = EnterpriseBo()

    def get_count(self, status=None):
        count = self.enterprise_bo.get_count(status)
        return count if count else 0

    def adds(self, datas):
        if not datas:
            LOG.error('DB: data is null.')
            return

        failure_list = list()
        success_list = list()
        for data in datas:
            if not data:
                continue

            if isinstance(data, str):
                data = dict(data)
            credit_code = data.get('credit_code')
            name = data.get('name')
            if not credit_code:
                failure_list.append(name)
                continue
            model = self.enterprise_bo.get_by_code(credit_code)
            if model:
                failure_list.append(name)
                continue

            new_model = self.enterprise_bo.new_mode()
            new_model.name = name
            new_model.phone = data.get('phone')
            new_model.email = data.get('email')
            new_model.tyc_url = data.get('tyc_url')
            new_model.company_url = data.get('company_url')
            new_model.address = data.get('address')
            new_model.register_funds = data.get('register_funds')
            new_model.paidin_funds = data.get('paidin_funds')
            new_model.establish_date = data.get('establish_date')
            new_model.status = data.get('status')
            new_model.credit_code = credit_code
            new_model.company_type = data.get('company_type')
            new_model.industry = data.get('industry')
            new_model.business_term = data.get('business_term')
            new_model.resume = data.get('resume')
            new_model.business_scope = data.get('business_scope')
            new_model.key = data.get('key')
            new_model.create_time = get_now()
            new_model.city =  data.get('city')
            new_model.sub_city = data.get('sub_city')
            try:
                self.enterprise_bo.add_model(new_model)
                success_list.append(name)
            except Exception as e:
                LOG.error('DB add error %s: %s' % (e, str(data)))
                failure_list.append(name)
        else:
            if success_list:
                LOG.info('success list:【%s】' % len(success_list))
            if failure_list:
                LOG.info('failure list:【%s】' % len(failure_list))
            return success_list, failure_list
