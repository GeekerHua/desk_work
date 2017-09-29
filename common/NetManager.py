# -*- coding: utf-8 -*-
# @Time    : 2017/9/21 14:59
# @Author  : Hua
# @Site    : 
# @File    : NetManager.py
# @Software: PyCharm
import os
import urllib2

from common.Util import RESTful
import logging

Base_Api = "https://api.github.com"


def renderUrl(api, **kwargs):
    """
    根据api和路径参数生成url
    :type api: str
    :rtype: str
    """
    for k, v in kwargs.iteritems():
        api = api.replace(':' + k, v, 1)
    url = Base_Api + api
    return url


def requestApi(url, method=RESTful.GET, data=None, headers=None):
    """

    :rtype: response.
    """
    defaultHeaders = {"Authorization": os.getenv('GitHub_Authorization')}
    headers = headers or {}
    headers.update(defaultHeaders)
    logging.info('request url %s, %s, headers = %s, data = %s', method, url, str(headers), data or 'None')
    request = urllib2.Request(url, headers=headers, data=data)
    request.get_method = lambda: method
    try:
        return urllib2.urlopen(request)
    except urllib2.HTTPError as e:
        # TODO: 处理不同的code if e.code == 400:
        print e, request.get_method(), url, headers, data
        return None
