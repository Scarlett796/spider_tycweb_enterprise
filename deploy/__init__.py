#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------
describe:
    

base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2020/7/4 3:41 PM"
    __mail__ = "gaoming971366@163.com"
--------------------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python __init__.py
# ------------------------------------------------------------
import os
import sys

from deploy.config import NAME, VERSION, KEYS, DEBUG,\
    STORE_DB, STORE_EXCEL, OUTPUT_BASE_DIR, RUN_MODE, \
    STORE_EXCEL, API_MODE, PAGINATION, IS_TEST_BREAK,\
    MIN_PAGE, MAX_PAGE
from deploy.utils.logger import logger as LOG
from deploy.utils.base_class import BASECLASS
from deploy.client.tianyancha import TianYanChaClient
from deploy.utils.to_excel import ToExcel
from deploy.utils.utils import get_now, get_excel_folder
from deploy.services.enterprise import EnterpriseService


# 支持协程
# import gevent
# from gevent import monkey; monkey.patch_all()

# 支持多进程
import multiprocessing


MAX_CPU = multiprocessing.cpu_count()


MODES = ['single', 'gevent', 'process']

ATTRS_DICT = {
    'name': "名称",
    'email': "邮箱",
    'phone': "电话",
    'tyc_url': "天眼查URL",
    'company_url': "公司官网",
    'address': "地址",
    'register_funds': "注册资金",
    'paidin_funds': "实缴资金",
    'establish_date': "注册日期",
    'status': "经营状态",
    'credit_code': "信用代码",
    'company_type': "公司类型",
    'industry': "所属行业",
    'business_term': "营业期限",
    'resume': "简述",
    'business_scope': "经营范围",
    'key': "搜索关键字"
}


class SpiderTYCClass(BASECLASS):
    """
    It is class
    to use spider tianyancha enterprise data
    """

    def __init__(self):
        self.name = NAME
        self.version = VERSION
        self.keys = KEYS
        if not self.keys:
            self._die('KEYS is null, exit')
        self.debug = DEBUG
        self.store_excel = STORE_EXCEL
        self.store_db = STORE_DB
        self.store_excel_dir = OUTPUT_BASE_DIR
        self.tyc_client = TianYanChaClient()
        self.excel_client = ToExcel()
        self.enterprise_service = EnterpriseService()
        self.__init_return_res()

    def __init_return_res(self):
        self.ret_res_list = list()


    def _die(self, message: str = None):
        if message:
            LOG.critical(message)
        os._exit(0)

    def _print_info(self, message):
        LOG.info('=' * 20 + message + '=' * 20)

    def single_run(self):
        """
        single mode to run
        :return: None
        """
        for key in self.keys:
            if not key:
                continue

            min_page, max_pagination = self.tyc_client.get_pagination(key)
            # page_count_max
            if max_pagination // PAGINATION == 0:
                page_count_max = 1
            else:
                if (max_pagination / PAGINATION) == max_pagination // PAGINATION:
                    page_count_max =  max_pagination // PAGINATION
                else:
                    page_count_max =  max_pagination // PAGINATION + 1
            if not MAX_PAGE:
                page_count_max = page_count_max
            else:
                if MAX_PAGE / PAGINATION == MAX_PAGE // PAGINATION:
                    page_count_max = MAX_PAGE // PAGINATION
                else:
                    page_count_max = MAX_PAGE // PAGINATION + 1
            # page_count_min
            if not MIN_PAGE:
                page_count_min = 0
            else:
                if MIN_PAGE / PAGINATION == MIN_PAGE // PAGINATION:
                    page_count_min = MIN_PAGE // PAGINATION
                else:
                    page_count_min = MIN_PAGE // PAGINATION + 1
            for i in range(page_count_min, page_count_max, 1):
                max_page = PAGINATION * i
                if max_page > max_pagination:
                    max_page = max_pagination
                self._print_info('[%s][%s]%s ~ %s' % (RUN_MODE, key, min_page, max_page))
                _res = self.tyc_client.work_by_key(key, min_page, max_page)

                if STORE_EXCEL:
                    to_excel_name = os.path.join(get_excel_folder(),
                                                 '%s[%s]-%s[%s~%s].xls' %
                                                 (get_now(), API_MODE, key, min_page, max_page))
                    self.excel_client.to_excel(_res, ATTRS_DICT, to_excel_name)
                    LOG.info(to_excel_name)

                if STORE_DB:
                    self.enterprise_service.adds(self.ret_res_list)
                    LOG.info('DB is finished: %s[%s ~ %s]' % ('_'.join(key), min_page, max_page))

                min_page = max_page + 1

    def process_run(self):
        """
        multiprocess mode to run
        :return: None
        """

        manager = multiprocessing.Manager()
        q = manager.Queue()

        pool = multiprocessing.Pool(processes=(MAX_CPU-1 if MAX_CPU > 2 else 1))
        LOG.info('run cpu count: %s' % (MAX_CPU-1 if MAX_CPU > 2 else 1))
        process = list()

        for key in self.keys:
            if not key:
                continue

            min_page, max_page = self.tyc_client.get_pagination(key)
            if MIN_PAGE:
                min_page = MIN_PAGE
            if MAX_PAGE:
                max_page = MAX_PAGE
            process.append(
                pool.apply_async(self.tyc_client.work_by_key, args=(key, min_page, max_page, q))
            )

        pool.close()
        pool.join()

        while 1:
            try:
                if q.empty():
                    break
                self.ret_res_list.append(q.get())
            except:
                continue

        if STORE_EXCEL:
            to_excel_name = os.path.join(get_excel_folder(),
                                         '%s[%s]-%s[%s~%s].xls' %
                                         (get_now(), API_MODE, '_'.join(self.keys), min_page, max_page))
            self.excel_client.to_excel(self.ret_res_list, ATTRS_DICT, to_excel_name)
            LOG.info(to_excel_name)
        if STORE_DB:
            self.enterprise_service.adds(self.ret_res_list)
            LOG.info('DB is finished: %s' % '_'.join(self.keys))

    def gevent_run(self):
        jobs = list()
        for key in self.keys:
            if not key:
                continue
        #     jobs.append(gevent.spawn(self.tyc_client.work_by_key, args=(key, ))
        # gevent.joinall(jobs)

    def init_run(self):
        if not RUN_MODE or RUN_MODE not in MODES:
            self._die('run node nit in [single, gevent, process], '
                      'please to set run mode at etc/config.yaml file.')

        if RUN_MODE == 'gevent':
            self.gevent_run()
        elif RUN_MODE == 'process':
            self.process_run()
        else:
            self.single_run()


def start():
    LOG.info('%s run start [IS TEST RUN: %s]......' % (NAME, IS_TEST_BREAK))
    SpiderTYCClass().init_run()
    LOG.info('%s run end [IS TEST RUN: %s]......' % (NAME, IS_TEST_BREAK))

