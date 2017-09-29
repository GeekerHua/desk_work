# -*- coding: utf-8 -*-
# @Time    : 2017/9/21 15:04
# @Author  : Hua
# @Site    : 
# @File    : Util.py
# @Software: PyCharm

class RESTful(object):
    GET = 'GET'
    POST = 'POST'
    PATCH = 'PATCH'


class SQLAction(object):
    insert = 'INSERT'
    update = 'UPDATE'
    execute = 'execute'
    executemany = 'executemany'
    create = 'create'
    queryAll = 'queryAll'



class NoAttributeError(Exception):
    pass

class NoRepoError(Exception):
    pass

class WrapperMethodError(Exception):
    pass