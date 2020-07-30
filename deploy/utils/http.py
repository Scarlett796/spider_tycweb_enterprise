#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------
describe:
    

base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2020/7/6 2:17 PM"
    __mail__ = "gaoming971366@163.com"
--------------------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python http.py
# ------------------------------------------------------------
import requests
import json
import sys


from deploy.config import IS_PROXY_RUN, PROXY_API
from deploy.utils.utils import random_sleep
from deploy.utils.logger import logger as LOG


def api_post(url, headers={}, data={},
             retry=1, resptype='json', **kwargs):
    """
    http post
    :param url: url
    :param headers: headers
    :param data: data
    :return: response
    """
    if not url:
        return False, 'api_post url is not allow null'

    if isinstance(data, dict):
        data = json.dumps(data)
    if not isinstance(headers, dict):
        headers = json.dumps(headers)

    try:
        if not IS_PROXY_RUN:
            response = requests.post(url=url, headers=headers,
                                     data=data, timeout=5)
        else:
            random_ip = get_random_proxy()
            proxies = {'http': random_ip} if random_ip else {}
            response = requests.post(url=url, headers=headers,
                                     data=data, timeout=5, proxies=proxies)
    except Exception as e:
        if retry <= 3:
            random_sleep(7, 7.5)
            api_post(url=url,
                     headers=headers,
                     data=data,
                     retry=retry + 1,
                     resptype=resptype)
        else:
            LOG.error(u'@@@@@ %s api_post error: %s' % (url, e))
            return False, []
    else:
        respcode = response.status_code
        if respcode != 200:
            return False, 'api_post response status code is: %s' % respcode
        elif respcode == 200 and resptype == 'raw':
            return True, response.raw
        elif respcode == 200 and resptype == 'content':
            return True, response.content
        elif respcode == 200 and resptype == 'json':
            return True, response.json()
        else:
            return True, response.text


def api_get(url,  headers={}, data={},
            retry=1, resptype='json', **kwargs):
    """
    http get
    :param url: url
    :param headers: headers
    :param data: data
    :return: response
    """
    if not url:
        return False, 'api_get url is not allow null'

    if isinstance(data, dict):
        data = json.dumps(data)
    if not isinstance(headers, dict):
        headers = json.dumps(headers)

    try:
        if not IS_PROXY_RUN:
            response = requests.get(url=url, headers=headers,
                                    data=data, timeout=5)
        else:
            random_ip = get_random_proxy()
            proxies = {'http': random_ip} if random_ip else {}
            response = requests.get(url=url, headers=headers,
                                    data=data, timeout=5, proxies=proxies)
    except Exception as e:
        if retry <= 3:
            random_sleep(7, 10)
            api_get(url, headers, data, retry=retry + 1, resptype=resptype)
        else:
            LOG.error(u'@@@@@ %s api_get error: %s' % (url, e))
            return False, []
    else:
        respcode = response.status_code
        if respcode != 200:
            if check_404code(response.text):
                return True, response.text
            return False, 'api_get response status code is: %s' % respcode
        elif respcode == 200 and resptype == 'raw':
            return True, response.raw
        elif respcode == 200 and resptype == 'content':
            return True, response.content
        elif respcode == 200 and resptype == 'json':
            return True, response.json()
        else:
            return True, response.text


def check_404code(content):
    if not content:
        return False

    # soup = BeautifulSoup(search_resp, 'lxml')
    # tags = soup.find_all('div', class_='f20 mb16 mt12 sec-c1 nodata_title_new')
    # if tags:
    #     if tags[0].get_text() == '抱歉，没有找到相关结果！' \
    #             or tags[0].string == '抱歉，没有找到相关结果！':
    return True


def get_random_proxy():
    """
    get random proxy from proxypool
    :return: proxy
    """
    try:
        res = requests.get(PROXY_API)
        return res.text.strip() if res.status_code ==200 else ''
    except:
        return ''
