#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------
describe:
    

base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2020/7/6 1:21 PM"
    __mail__ = "gaoming971366@163.com"
--------------------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python tianyancha.py
# ------------------------------------------------------------
import sys
from urllib import parse
from bs4 import BeautifulSoup

from deploy.config import RUN_MODE, API_MODE, TYC_COOKIE, \
    TYC_SEARCH_API, \
    TYC_PRO_SEARCH_API, TYC_PRO_DETAIL_API, IS_TEST_BREAK
from deploy.utils.http import api_get
from deploy.utils.logger import logger as LOG
from deploy.utils.utils import random_sleep



class TianYanChaClient(object):
    """
    tianyancha client
    """

    def __init__(self, min_page=0, max_page=5):
        super(object, self).__init__()
        self.MAX_PAGE = max_page
        self.MIN_PAGE = min_page
        self._init_header()

    def _init_header(self):
        if API_MODE == 'tyc':
            host = 'www.tianyancha.com'
        elif API_MODE == 'pro':
            host = 'pro.tianyancha.com'
        else:
            host = 'www.tianyancha.com'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            "version": "TYC-XCX-WX",
            "Host": host,
            "Cookie": TYC_COOKIE,
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "document"
        }

    def get_pagination(self, key):
        min_page = 0
        max_page = 5
        if not key:
            return min_page, max_page

        if API_MODE == 'tyc':
            return min_page, max_page
        elif API_MODE == 'pro':
            url = '%s/p%s?key=%s' % (TYC_PRO_SEARCH_API, '0', parse.quote(key))
            is_ok, search_resp = api_get(url=url,
                                         headers=self.headers,
                                         data={},
                                         resptype='text')

            soup = BeautifulSoup(search_resp, 'lxml')
            search_pagination = soup.find_all('div', class_='search-pagination')

            def while_req(url):
                sub_is_ok, sub_search_resp = api_get(url=url,
                                         headers=self.headers,
                                         data={},
                                         resptype='text')
                return sub_is_ok, sub_search_resp

            # 添加手动验证功能
            if len(search_pagination) == 0 or not is_ok:
                while 1:
                    if is_ok and len(search_pagination) > 0:
                        break
                    else:
                        LOG.critical('验证############### %s ###############' % url)
                        random_sleep(20,25)
                        is_ok, search_resp = while_req(url)
                        soup = BeautifulSoup(search_resp, 'lxml')
                        search_pagination = soup.find_all('div', class_='search-pagination')

            l = len(search_pagination[0].find_all('a'))
            for index_a, a in enumerate(search_pagination[0].find_all('a')):
                if index_a == (l - 2):
                    max_page = a.string.strip()
                    if max_page.find('...') > -1:
                        max_page = max_page.split('...')[1]
                        if isinstance(max_page, str):
                            max_page = int(max_page)
                    break
            LOG.info('[%s] pagination max: %s' % (key, max_page))
            return min_page, max_page

    def work_by_key(self, key, min_page=0, max_page=5, queue=None):
        ret_res = list()
        if not key:
            LOG.error("【%s】key is null, no work." % RUN_MODE)
            return ret_res

        if not min_page:
            min_page = self.MIN_PAGE
        if not max_page:
            max_page = self.MAX_PAGE

        LOG.info('%s[%s ~ %s]' % (key, min_page, max_page))
        # page
        for page in range(min_page, max_page, 1):
            if API_MODE == 'tyc':
                url = '%s/p%s?key=%s' % (TYC_SEARCH_API, page, parse.quote(key))
            elif API_MODE == 'pro':
                url = '%s/p%s?key=%s' % (TYC_PRO_SEARCH_API, page, parse.quote(key))
            else:
                LOG.critical('====== API_MODE is not in [tyc, pro] ======')
                sys.exit(1)
            LOG.info('%s[%s]%s' % (key, API_MODE, url))

            is_ok, search_resp = api_get(url=url,
                                         headers=self.headers,
                                         data={},
                                         resptype='text')

            if not is_ok:
                continue

            soup = BeautifulSoup(search_resp, 'lxml')
            tags = soup.find_all('a', attrs={"tyc-event-ch": "CompanySearch.Company"})

            def while_req(url):
                sub_is_ok, sub_search_resp = api_get(url=url,
                                         headers=self.headers,
                                         data={},
                                         resptype='text')
                return sub_is_ok, sub_search_resp

            # 添加手动验证功能
            if len(tags) == 0:
                while 1:
                    if is_ok and len(tags) > 0:
                        break
                    else:
                        LOG.critical('验证############### %s ###############' % url)
                        random_sleep(20,25)
                        is_ok, search_resp = while_req(url)
                        soup = BeautifulSoup(search_resp, 'lxml')
                        tags = soup.find_all('a', attrs={"tyc-event-ch": "CompanySearch.Company"})

            for tag in tags:
                if not tag or not tag.attrs.get('href'):
                    continue

                res_dict = dict()
                if API_MODE == 'tyc':
                    tyc_url = tag.get('href').strip()
                elif API_MODE == 'pro':
                    tyc_url = '%s%s/background' % (TYC_PRO_DETAIL_API, tag.get('href').strip())
                else:
                    tyc_url = ''
                res_dict['tyc_url'] = tyc_url
                res_dict['name'] = tag.get_text().strip()
                res_dict['key'] = key
                detail_res = list()
                if API_MODE == 'tyc':
                    detail_res = self.detail_by_url(res_dict.get('tyc_url'))
                elif API_MODE == 'pro':
                    detail_res = self.detail_pro_by_url(res_dict.get('tyc_url'))
                res_dict.update(detail_res)
                print('%s[%s] %s' % (res_dict['name'], str(True if res_dict else False), res_dict['tyc_url']))
                ret_res.append(res_dict)
                if queue:
                    queue.put(res_dict)
                random_sleep(3.2, 4.5)
                if IS_TEST_BREAK:
                    break
            if IS_TEST_BREAK:
                break
        return ret_res

    def detail_by_url(self, comp_url: str):
        detail_res = dict()
        if not comp_url:
            return detail_res

        is_ok, search_resp = api_get(url=comp_url,
                                     headers=self.headers,
                                     data={},
                                     resptype='text')
        if not is_ok:
            return detail_res

        soup = BeautifulSoup(search_resp, 'lxml')

        # detail: 电话 邮箱 公司官网 地址 简介
        detail_div = soup.find_all('div', class_="detail")

        def while_req(url):
            sub_is_ok, sub_search_resp = api_get(url=url,
                                     headers=self.headers,
                                     data={},
                                     resptype='text')
            return sub_is_ok, sub_search_resp

        # 添加手动验证功能
        if not detail_div:
            while 1:
                if is_ok and detail_div:
                    break
                else:
                    LOG.critical('验证############### %s ###############' % comp_url)
                    random_sleep(20, 25)
                    is_ok, search_resp = while_req(comp_url)
                    soup = BeautifulSoup(search_resp, 'lxml')
                    detail_div = soup.find_all('div', class_="detail")

        for div in detail_div[0].find_all('div'):
            if not div:
                continue

            # f0 电话 && 邮箱
            if div.get('class') == ['f0']:
                for big_index, big_child in enumerate(div):
                    if big_index == 0:
                        for index, child in enumerate(big_child.children):
                            if index == 1:
                                detail_res['phone'] = child.get_text().strip() or '-'
                                break
                    elif big_index == 1:
                        for index, child in enumerate(big_child.children):
                            if index == 1:
                                detail_res['email'] = child.get_text().strip() or '-'
                                break
                    else:
                        break
            # 公司官网 && 地址
            elif div.get('class') == ['f0', 'clearfix']:
                for big_index, big_child in enumerate(div):
                    if big_index == 0:
                        for index, child in enumerate(big_child.children):
                            if index == 1:
                                detail_res['company_url'] = child.get_text().strip() or '-'
                                break
                    elif big_index == 1:
                        for index, child in enumerate(big_child.children):
                            if index == 1:
                                for small_index, small_child in enumerate(child.children):
                                    if small_index == 0:
                                        detail_res['address'] = small_child.get_text().strip() or '-'
                                        break
                                break
                    else:
                        break
            # 简介
            elif div.get('class') == ['summary']:
                for big_index, big_child in enumerate(div):
                    if big_index == 0:
                        resume = big_child.string
                        if resume:
                            resume = resume.strip()
                        detail_res['resume'] = resume or '-'
                        break
                    else:
                        break
            else:
                continue

        # detail-list:
        detail_list_div = soup.find_all('div', class_="detail-list")
        if not detail_list_div:
            return detail_res

        for div in detail_list_div[0].find_all('div'):
            if not div:
                continue

            if div.get('tyc-event-ch') == 'CompangyDetail.gongshangxinxin':
                for index_1, child_1 in enumerate(div.find_all('div', recursive=False)):
                    if index_1 == 1:
                        for index_1_1, child_1_1 in enumerate(child_1):
                            if index_1_1 == 2:
                                for index_tr, tr in enumerate(child_1_1.find_all('tr')):
                                    if index_tr == 0:
                                        for index_td, td in enumerate(tr.find_all('td')):
                                            if index_td == 1:  # 注册资本
                                                detail_res['register_funds'] = td.get_text().strip() or '-'
                                            elif index_td == 3:  # 实缴资金
                                                detail_res['paidin_funds'] = td.get_text().strip() or '-'
                                    elif index_tr == 1:
                                        for index_td, td in enumerate(tr.find_all('td')):
                                            if index_td == 1:  # 成立日期
                                                detail_res['establish_date'] = td.get_text().strip() or '-'
                                            elif index_td == 3:  # 经营状态
                                                detail_res['status'] = td.get_text().strip() or '-'
                                    elif index_tr == 2:
                                        for index_td, td in enumerate(tr.find_all('td')):
                                            if index_td == 1:  # 信用代码
                                                detail_res['credit_code'] = td.get_text().strip() or '-'
                                    elif index_tr == 4:
                                        for index_td, td in enumerate(tr.find_all('td')):
                                            if index_td == 1:  # 公司类型
                                                detail_res['company_type'] = td.get_text().strip() or '-'
                                            elif index_td == 3:  # 行业
                                                detail_res['industry'] = td.get_text().strip() or '-'
                                    elif index_tr == 6:
                                        for index_td, td in enumerate(tr.find_all('td')):
                                            if index_td == 1:  # 营业期限
                                                detail_res['business_term'] = td.get_text().strip() or '-'
                                    elif index_tr == 10:
                                        for index_td, td in enumerate(tr.find_all('td')):
                                            if index_td == 1:  # 经营范围
                                                detail_res['business_scope'] = td.get_text().strip() or '-'

                        break
                break
        return detail_res

    def detail_pro_by_url(self, comp_url: str):
        detail_res = dict()
        if not comp_url:
            return detail_res

        is_ok, search_resp = api_get(url=comp_url,
                                     headers=self.headers,
                                     data={},
                                     resptype='text')
        if not is_ok:
            print('X-' * 100)
            print(comp_url)
            return detail_res

        soup = BeautifulSoup(search_resp, 'lxml')

        # detail: 电话 邮箱 公司官网 地址 简介
        detail_div = soup.find_all('div', class_="ie9Style")

        def while_req(url):
            sub_is_ok, sub_search_resp = api_get(url=url,
                                     headers=self.headers,
                                     data={},
                                     resptype='text')
            return sub_is_ok, sub_search_resp

        # 添加手动验证功能
        if not detail_div:
            while 1:
                if is_ok and detail_div:
                    break
                else:
                    LOG.critical('验证############### %s ###############' % comp_url)
                    random_sleep(20, 25)
                    is_ok, search_resp = while_req(comp_url)
                    soup = BeautifulSoup(search_resp, 'lxml')
                    detail_div = soup.find_all('div', class_="ie9Style")

        # 0 企业缩略图 1 基础信息 2 下载
        for index, div in enumerate(detail_div[1].find_all('div', recursive=False)):
            if not div:
                continue

            # 电话 && 邮箱
            if index == 1:
                for big_index, big_child in enumerate(div):
                    if big_index == 0:
                        for sub_index, child in enumerate(big_child.children):
                            if sub_index == 1:
                                detail_res['phone'] = child.get_text().strip() or '-'
                    elif big_index == 1:
                        for sub_index, child in enumerate(big_child.children):
                            if sub_index == 1:
                                detail_res['email'] = child.get_text().strip() or '-'
            # 公司官网 && 地址
            elif index == 2:
                for big_index, big_child in enumerate(div):
                    if big_index == 0:
                        for sub_index, child in enumerate(big_child.children):
                            if sub_index == 1:
                                detail_res['company_url'] = child.get_text().strip() or '-'
                    elif big_index == 1:
                        for sub_index, child in enumerate(big_child.children):
                            if sub_index == 1:
                                detail_res['address'] = child.get_text().strip() or '-'
                                break
            # 简介
            elif index == 3:
                for big_index, big_child in enumerate(div):
                    if big_index == 0:
                        for sub_index, sub_child in enumerate(big_child):
                            if sub_index ==1:
                                resume = sub_child.string
                                if resume:
                                    resume = resume.strip()
                                detail_res['resume'] = resume or '-'
                                break
                    break
            else:
                continue

        # detail-list: 信用代码 公司类型 所属行业 营业期限 实缴资本 经营范围
        detail_list_div = soup.find_all('div', class_='base0910')
        if not detail_list_div:
            return detail_res

        for index_tr, tr in enumerate(detail_list_div[0].find_all('tr')):
            if not tr:
                continue

            if index_tr == 1:
                for index_td, td in enumerate(tr.find_all('td', recursive=False)):
                    if index_td == 1:  # 信用代码
                        detail_res['credit_code'] = td.get_text().strip() or '-'
                    elif index_td == 3:  # 公司类型
                        detail_res['company_type'] = td.get_text().strip() or '-'
            elif index_tr == 2:
                for index_td, td in enumerate(tr.find_all('td', recursive=False)):
                    if index_td == 3:  # 所属行业
                        detail_res['industry'] = td.get_text().strip() or '-'
            elif index_tr == 3:
                for index_td, td in enumerate(tr.find_all('td', recursive=False)):
                    if index_td == 1:  # 营业期限
                        detail_res['business_term'] = td.get_text().strip() or '-'
            elif index_tr == 4:
                for index_td, td in enumerate(tr.find_all('td', recursive=False)):
                    if index_td == 3:  # 实缴资本
                        detail_res['paidin_funds'] = td.get_text().strip() or '-'
            elif index_tr == 8:
                for index_td, td in enumerate(tr.find_all('td', recursive=False)):
                    if index_td == 1:  # 经营范围
                        detail_res['business_scope'] = td.get_text().strip() or '-'

        # detail-list: 注册资金 注册日期 经营状态
        detail_list_div_1 = soup.find_all('div', class_='baseInfo_model2017')
        if not detail_list_div:
            return detail_res

        for index_table, table in enumerate(detail_list_div_1[0].find_all('table')):
            if not table:
                continue

            if index_table == 1:
                for index_tr, tr in enumerate(table.find_all('tr')):
                    if index_tr == 1:
                        for index_td, td in enumerate(tr.find_all('td', recursive=False)):
                            if index_td == 1:
                                for index_td_span, td_span in enumerate(td.find_all('span')):
                                    if index_td_span == 1:
                                        detail_res['register_funds'] = td_span.get_text().strip() or '-'
                    elif index_tr == 2:
                        for index_td, td in enumerate(tr.find_all('td', recursive=False)):
                            if index_td == 0:
                                for index_td_span, td_span in enumerate(td.find_all('span')):
                                    if index_td_span == 1:
                                        detail_res['establish_date'] = td_span.get_text().strip() or '-'
                    elif index_tr == 3:
                        for index_td, td in enumerate(tr.find_all('td', recursive=False)):
                            if index_td == 0:
                                for index_td_div, td_div in enumerate(td.find_all('div', recursive=False)):
                                    if index_td_div == 0:
                                        for index_td_div_span, td_div_span in enumerate(td_div.find_all('span', recursive=False)):
                                            if index_td_div_span == 1:
                                                detail_res['status'] = td_div_span.get_text().strip() or '-'

        return detail_res
