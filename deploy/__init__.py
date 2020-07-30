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

from deploy.config import NAME, VERSION, KEYS, DEBUG, \
    STORE_DB, STORE_EXCEL, OUTPUT_BASE_DIR, RUN_MODE, \
    STORE_EXCEL, API_MODE, PAGINATION, IS_TEST_BREAK, MIN_PAGE, MAX_PAGE, \
    IS_PLUS_CITY, IS_PLUS_CITY_SUB, PLUS_CITYS
from deploy.utils.logger import logger as LOG
from deploy.utils.base_class import BASECLASS
from deploy.client.tianyancha import TianYanChaClient
from deploy.utils.to_excel import ToExcel
from deploy.utils.utils import get_now, get_excel_folder
from deploy.services.enterprise import EnterpriseService
from deploy.services.citys import CitysService

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
    'key': "搜索关键字",
    'city': "省份",
    'sub_city': "市"
}

CITYS_ATTRS_LIST = ['id', 'name', 'full_name', 'code', 'is_cg']

NO_SUB_CITYS = [33, 34, 35, '33', '34', '35']

MIN_CITY_ID = 1
MAX_CITY_ID = 35


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
        self.citys_service = CitysService()
        self.citys_dict = dict()
        self.sub_citys_dict = dict()
        self.sub_citys_mapping = dict()
        self.NO_SUB_CITYS = self.__init_no_sub_citys()
        self.__init_return_res()
        self.__init_citys()
        self.__init_q()

    def __init_return_res(self):
        self.ret_res_list = list()

    def __init_q(self):
        manager = multiprocessing.Manager()
        q = manager.Queue()
        self.q = q

    def __init_citys(self):
        # 省份
        citys = dict()
        for x in range(MIN_CITY_ID, MAX_CITY_ID + 1, 1):
            city_info = self.citys_service.get_by_id(x)
            if not city_info:
                continue
            d = dict()
            d['id'] = city_info.id
            d['name'] = city_info.name
            d['full_name'] = city_info.full_name
            d['parent_id'] = city_info.parent_id
            d['code'] = city_info.code
            d['is_cg'] = city_info.is_cg
            citys[x] = d
        self.citys_list = citys
        # 市
        sub_citys_map = dict()
        sub_citys = dict()
        for x in range(MIN_CITY_ID, MAX_CITY_ID + 1, 1):
            city_info = self.citys_service.get_by_id(x)
            if not city_info:
                continue
            sub_objs = self.citys_service.get_subobj_by_parid(x)
            if not sub_objs:
                continue

            dl = list()
            for sub_obj in sub_objs:
                if not sub_obj:
                    continue
                d = dict()
                d['id'] = sub_obj.id
                d['name'] = sub_obj.name
                d['full_name'] = sub_obj.full_name
                d['parent_id'] = sub_obj.parent_id
                d['code'] = sub_obj.code
                d['is_cg'] = sub_obj.is_cg
                dl.append(d)
                sub_citys[d.get('id')] = d
            sub_citys_map[x] = dl
        self.sub_citys_mapping = sub_citys_map
        self.sub_citys_dict = sub_citys

    def __init_no_sub_citys(self):
        return self.citys_service.get_no_sub_citys()

    def _die(self, message: str = None):
        if message:
            LOG.critical(message)
        os._exit(0)

    def _print_info(self, message):
        LOG.info('=' * 20 + message + '=' * 20)

    def to_store(self, keys, min_page, max_page, datas=None, excelname=None):
        _keys = list()
        if isinstance(keys, list):
            _keys = keys
        else:
            _keys.append(keys)
        _data = datas if datas else self.ret_res_list
        if STORE_EXCEL:
            if (min_page and max_page):
                to_excel_name = os.path.join(get_excel_folder(), '%s[%s]-%s[%s~%s].xls'
                                             % (get_now(), API_MODE, '_'.join(_keys), min_page, max_page))
            else:
                to_excel_name = os.path.join(get_excel_folder(), '%s[%s]-%s[ALL].xls' % (get_now(), API_MODE, '_'.join(_keys)))
            self.excel_client.to_excel(_data, ATTRS_DICT, to_excel_name)
            LOG.info("Excel is finished[%s ~ %s]: %s" % (min_page, max_page, to_excel_name))
        if STORE_DB:
            self.enterprise_service.adds(_data)
            LOG.info('DB is finished[%s ~ %s]: %s' % (min_page, max_page, '_'.join(_keys))) \
                if (MIN_PAGE and MAX_PAGE) else LOG.info('DB is finished[ALL]: %s' % ('_'.join(_keys)))

    def _is_not_max_range_die(self, max_range):
        if not max_range:
            LOG.error("It's not have max range")
            sys.exit()

    def _single_by_key(self):
        for key in self.keys:
            if not key:
                continue

            min_page, max_page, max_pagination, max_range = self.tyc_client.get_pagination(key)
            self._is_not_max_range_die(max_range)
            LOG.info('[%s][%s]spider page: %s ~ %s ||| max_pagination: %s ||| max range: %s'
                     % (RUN_MODE, key, min_page, max_page, max_pagination, max_range))

            if not isinstance(max_pagination, int):
                max_pagination = int(max_pagination)
            for i in range(0, max_range, 1):
                max_page = PAGINATION + min_page
                if max_page > max_pagination:
                    max_page = max_pagination
                self._print_info('[%s][%s]%s ~ %s' % (RUN_MODE, key, min_page, max_page))
                _res = self.tyc_client.work_by_key(key, min_page, max_page)
                self.to_store(key, min_page, max_page, datas=_res)
                min_page = max_page + 1

    def _single_by_key_city(self):
        for key in self.keys:
            if not key:
                continue
            for cid in PLUS_CITYS:
                if not cid:
                    continue
                if not isinstance(cid, int):
                    cid = int(cid)

                city_info = self.citys_list.get(cid)
                if not city_info:
                    LOG.info('@@@@@: %s is not have city information, exit...' % cid)
                    sys.exit(1)

                city_full_name = city_info.get('full_name')
                min_page, max_page, max_pagination, max_range = self.tyc_client.get_pagination(key, _type='city',
                                                                                               city_id=cid, cityes=self.citys_list)

                self._is_not_max_range_die(max_range)
                LOG.info('[%s][%s][%s]spider page: %s ~ %s ||| max_pagination: %s ||| max range: %s'
                         % (RUN_MODE, key, city_full_name, min_page, max_page, max_pagination, max_range))
                if not isinstance(max_pagination, int):
                    max_pagination = int(max_pagination)
                for i in range(0, max_range, 1):
                    max_page = PAGINATION + min_page
                    if max_page > max_pagination:
                        max_page = max_pagination
                    self._print_info('[%s][%s][%s]%s ~ %s' % (RUN_MODE, key, city_full_name, min_page, max_page))
                    _res = self.tyc_client.work_by_key(key, min_page, max_page, cid=cid, city_info=city_info)
                    self.to_store(key, min_page, max_page, datas=_res)
                    min_page = max_page + 1

    def _single_by_key_sub_city(self):
        for key in self.keys:
            if not key:
                continue

            for cid in PLUS_CITYS:
                if not cid or not (cid in self.NO_SUB_CITYS):
                    continue
                if not isinstance(cid, int):
                    cid = int(cid)

                city_info = self.citys_list.get(cid)
                if not city_info:
                    LOG.info('@@@@@: %s is not have city information, exit...' % cid)
                    sys.exit(1)

                city_full_name = city_info.get('full_name')
                sub_city_infos = self.sub_citys_mapping.get(cid)

                if not sub_city_infos:
                    LOG.info('%s is not have sub_city_infos, exit...' % cid)
                    sys.exit(1)

                for sub_city_info in sub_city_infos:
                    if not sub_city_info:
                        continue
                    sub_city_id = sub_city_info.get('id')
                    sub_city_full_name = sub_city_info.get('full_name')
                    min_page, max_page, max_pagination, max_range = self.tyc_client.get_pagination(key, _type='sub_city',
                                                                                                   city_id=cid,
                                                                                                   sub_city_id=sub_city_id,
                                                                                                   cityes=self.citys_list,
                                                                                                   sub_city_info=sub_city_info)
                    if not isinstance(max_pagination, int):
                        max_pagination = int(max_pagination)
                    self._is_not_max_range_die(max_range)
                    LOG.info('[%s][%s][%s - %s]spider page: %s ~ %s ||| max_pagination: %s ||| max range: %s'
                             % (RUN_MODE, key, city_full_name, sub_city_full_name, min_page, max_page, max_pagination, max_range))

                    for i in range(0, max_range, 1):
                        max_page = PAGINATION + min_page
                        if max_page > max_pagination:
                            max_page = max_pagination
                        self._print_info('[%s][%s][%s]%s ~ %s' % (RUN_MODE, key, city_full_name, min_page, max_page))
                        _res = self.tyc_client.work_by_key(key, min_page, max_page, cid=cid, sub_cid=sub_city_id,
                                                           city_info=city_info, sub_city_info=sub_city_info)
                        self.to_store(key, min_page, max_page, datas=_res)
                        min_page = max_page + 1

    def _single_by_key_only_sub_city(self):

        for key in self.keys:
            if not key:
                continue

            for sub_cid in PLUS_CITYS:
                if not sub_cid:
                    continue
                if not isinstance(sub_cid, int):
                    sub_cid = int(sub_cid)

                sub_city_info = self.sub_citys_dict.get(sub_cid)
                if not sub_city_info:
                    LOG.info('@@@@@: %s is not have sub_city information, exit...' % sub_cid)
                    sys.exit(1)
                sub_city_pid = sub_city_info.get('parent_id')
                city_info = self.citys_list.get(sub_city_pid)
                if not city_info:
                    LOG.info('@@@@@: %s is not have parent city information, exit...' % sub_cid)
                    sys.exit(1)

                city_id = city_info.get('id')
                city_full_name = city_info.get('full_name')
                sub_city_id = sub_city_info.get('id')
                sub_city_full_name = sub_city_info.get('full_name')
                min_page, max_page, max_pagination, max_range = self.tyc_client.get_pagination(key, _type='sub_city',
                                                                                               city_id=city_id,
                                                                                               sub_city_id=sub_city_id,
                                                                                               cityes=self.citys_list,
                                                                                               sub_city_info=sub_city_info)
                max_pagination = int(max_pagination)
                LOG.info('[%s][%s][%s-%s]spider page: %s ~ %s ||| max_pagination: %s ||| max range: %s'
                         % (RUN_MODE, key, city_full_name, sub_city_full_name, min_page, max_page, max_pagination, max_range))
                self._is_not_max_range_die(max_range)

                for i in range(0, max_range, 1):
                    max_page = PAGINATION + min_page
                    if max_page > max_pagination:
                        max_page = max_pagination
                    self._print_info('[%s][%s][%s]%s ~ %s' % (RUN_MODE, key, city_full_name, min_page, max_page))
                    _res = self.tyc_client.work_by_key(key, min_page, max_page, cid=city_id, sub_cid=sub_city_id,
                                                       city_info=city_info, sub_city_info=sub_city_info)
                    self.to_store(key, min_page, max_page, datas=_res)
                    min_page = max_page + 1

    def single_run(self):
        """
        single mode to run
        :return: None
        """
        if not IS_PLUS_CITY and not IS_PLUS_CITY_SUB:
            self._single_by_key()
        elif IS_PLUS_CITY and not IS_PLUS_CITY_SUB:
            self._single_by_key_city()
        elif IS_PLUS_CITY and IS_PLUS_CITY_SUB:
            self._single_by_key_sub_city()
        elif not IS_PLUS_CITY and IS_PLUS_CITY_SUB:
            self._single_by_key_only_sub_city()

    def _process_by_key(self):
        pool = multiprocessing.Pool(processes=(MAX_CPU - 1 if MAX_CPU > 2 else 1))
        LOG.info('Main process: %s, run cpu count: %s' % (os.getpid(), (MAX_CPU - 1 if MAX_CPU > 2 else 1)))
        process = list()

        for key in self.keys:
            if not key:
                continue

            min_page, max_page, max_pagination, max_range = self.tyc_client.get_pagination(key)
            LOG.info('[%s][%s]spider page: %s ~ %s ||| max_pagination: %s ||| max range: %s'
                     % (RUN_MODE, key, min_page, max_page, max_pagination, max_range))
            if not max_range:
                LOG.error("It's not have max range")
                sys.exit()

            for i in range(0, max_range, 1):
                max_page = min_page + PAGINATION
                if max_page > max_pagination:
                    max_page = max_pagination
                process.append(
                    pool.apply_async(self.tyc_client.work_by_key, args=(key, min_page, max_page,
                                                                        self.q, self.citys_list, self.sub_citys_mapping))
                )
                min_page = max_page + 1

        pool.close()
        pool.join()

        while 1:
            try:
                if self.q.empty():
                    break
                self.ret_res_list.append(self.q.get_nowait())
            except:
                pass

        self.to_store(self.keys, MIN_PAGE, MAX_PAGE)

    def _process_by_key_city(self):
        pool = multiprocessing.Pool(processes=(MAX_CPU - 1 if MAX_CPU > 2 else 1))
        LOG.info('Main process: %s, run cpu count: %s' % (os.getpid(), (MAX_CPU - 1 if MAX_CPU > 2 else 1)))
        process = list()

        for key in self.keys:
            if not key:
                continue

            for cid in PLUS_CITYS:
                if not cid:
                    continue
                if not isinstance(cid, int):
                    cid = int(cid)

                city_info = self.citys_list.get(cid)
                if not city_info:
                    LOG.info('@@@@@: %s is not have city information, exit...' % cid)
                    sys.exit(1)

                city_full_name = city_info.get('full_name')
                min_page, max_page, max_pagination, max_range = \
                    self.tyc_client.get_pagination(key, _type='city', city_id=cid, cityes=self.citys_list)

                LOG.info('[%s][%s][%s]spider page: %s ~ %s ||| max_pagination: %s ||| max range: %s'
                         % (RUN_MODE, key, city_full_name, min_page, max_page, max_pagination, max_range))
                self._is_not_max_range_die(max_range)

                for i in range(0, max_range, 1):
                    max_page = min_page + PAGINATION
                    if max_page > max_pagination:
                        max_page = max_pagination
                    process.append(
                        pool.apply_async(self.tyc_client.work_by_key, args=(key, min_page, max_page, 'city',
                                                                            self.q, cid, None, city_info, None))
                    )
                    min_page = max_page + 1

        pool.close()
        pool.join()

        while 1:
            try:
                if self.q.empty():
                    break
                self.ret_res_list.append(self.q.get_nowait())
            except:
                pass

        self.to_store(self.keys, MIN_PAGE, MAX_PAGE)

    def _process_by_key_sub_city(self):
        pool = multiprocessing.Pool(processes=(MAX_CPU - 1 if MAX_CPU > 2 else 1))
        LOG.info('Main process: %s, run cpu count: %s' % (os.getpid(), (MAX_CPU - 1 if MAX_CPU > 2 else 1)))
        process = list()

        for key in self.keys:
            if not key:
                continue

            for cid in PLUS_CITYS:
                if not cid or (cid in self.NO_SUB_CITYS):
                    continue
                if not isinstance(cid, int):
                    cid = int(cid)

                city_info = self.citys_list.get(cid)
                if not city_info:
                    LOG.info('@@@@@: %s is not have city information, exit...' % cid)
                    sys.exit(1)
                city_full_name = city_info.get('full_name')
                sub_city_infos = self.sub_citys_mapping.get(cid)

                if not sub_city_infos:
                    LOG.info('%s is not have sub_city_infos, exit...' % cid)
                    sys.exit(1)

                for sub_city_info in sub_city_infos:
                    if not sub_city_info:
                        continue
                    sub_city_id = sub_city_info.get('id')
                    sub_city_full_name = sub_city_info.get('full_name')
                    min_page, max_page, max_pagination, max_range = self.tyc_client.get_pagination(key,
                                                                                                   _type='sub_city',
                                                                                                   city_id=cid,
                                                                                                   sub_city_id=sub_city_id,
                                                                                                   cityes=self.citys_list,
                                                                                                   sub_city_info=sub_city_info)
                    if not isinstance(max_pagination, int):
                        max_pagination = int(max_pagination)

                    LOG.info('[%s][%s][%s - %s]spider page: %s ~ %s ||| max_pagination: %s ||| max range: %s'
                             % (RUN_MODE, key, city_full_name, sub_city_full_name, min_page, max_page, max_pagination, max_range))
                    self._is_not_max_range_die(max_range)

                    for i in range(0, max_range, 1):
                        max_page = min_page + PAGINATION
                        if max_page > max_pagination:
                            max_page = max_pagination
                        process.append(
                            pool.apply_async(self.tyc_client.work_by_key, args=(key, min_page, max_page, 'sub_city',
                                                                                self.q, cid, sub_city_id, city_info, sub_city_info))
                        )
                        min_page = max_page + 1

        pool.close()
        pool.join()

        while 1:
            try:
                if self.q.empty():
                    break
                self.ret_res_list.append(self.q.get_nowait())
            except:
                pass

        self.to_store(self.keys, MIN_PAGE, MAX_PAGE)

    def _process_by_key_only_sub_city(self):
        pool = multiprocessing.Pool(processes=(MAX_CPU - 1 if MAX_CPU > 2 else 1))
        LOG.info('Main process: %s, run cpu count: %s' % (os.getpid(), (MAX_CPU - 1 if MAX_CPU > 2 else 1)))
        process = list()

        for key in self.keys:
            if not key:
                continue

            for sub_cid in PLUS_CITYS:
                if not sub_cid:
                    continue
                if not isinstance(sub_cid, int):
                    sub_cid = int(sub_cid)

                sub_city_info = self.sub_citys_dict.get(sub_cid)
                if not sub_city_info:
                    LOG.info('@@@@@: %s is not have sub_city information, exit...' % sub_cid)
                    sys.exit(1)
                sub_city_pid = sub_city_info.get('parent_id')
                city_info = self.citys_list.get(sub_city_pid)
                if not city_info:
                    LOG.info('@@@@@: %s is not have parent city information, exit...' % sub_cid)
                    sys.exit(1)

                city_id = city_info.get('id')
                city_full_name = city_info.get('full_name')
                sub_city_id = sub_city_info.get('id')
                min_page, max_page, max_pagination, max_range = self.tyc_client.get_pagination(key, _type='sub_city',
                                                                                               city_id=city_id,
                                                                                               sub_city_id=sub_city_id,
                                                                                               cityes=self.citys_list,
                                                                                               sub_city_info=sub_city_info)
                max_pagination = int(max_pagination)
                LOG.info('[%s][%s][%s-%s]spider page: %s ~ %s ||| max_pagination: %s ||| max range: %s'
                         % (RUN_MODE, key, city_full_name, sub_city_info.get('full_name'), min_page, max_page, max_pagination, max_range))
                self._is_not_max_range_die(max_range)

                for i in range(0, max_range, 1):
                    max_page = min_page + PAGINATION
                    if max_page > max_pagination:
                        max_page = max_pagination
                    process.append(
                        pool.apply_async(self.tyc_client.work_by_key, args=(key, min_page, max_page, 'city',
                                                                            self.q, city_id, sub_city_id, city_info, sub_city_info))
                    )
                    min_page = max_page + 1

        pool.close()
        pool.join()

        while 1:
            try:
                if self.q.empty():
                    break
                self.ret_res_list.append(self.q.get_nowait())
            except:
                pass

        self.to_store(self.keys, MIN_PAGE, MAX_PAGE)

    def process_run(self):
        """
        multiprocess mode to run
        :return: None
        """
        if not IS_PLUS_CITY and not IS_PLUS_CITY_SUB:  # key
            self._process_by_key()
        elif IS_PLUS_CITY and not IS_PLUS_CITY_SUB:  # key + 省份
            self._process_by_key_city()
        elif IS_PLUS_CITY and IS_PLUS_CITY_SUB:  # key + 省（all市）
            self._process_by_key_sub_city()
        elif not IS_PLUS_CITY and IS_PLUS_CITY_SUB:  # key + 市
            self._process_by_key_only_sub_city()

    def gevent_run(self):
        jobs = list()
        for key in self.keys:
            if not key:
                continue
                #     jobs.append(gevent.spawn(self.tyc_client.work_by_key, args=(key, 0, 10)))
                # gevent.joinall(jobs)
                # for job in jobs:
                #     print(job)

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
