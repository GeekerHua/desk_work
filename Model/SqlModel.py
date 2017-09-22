# -*- coding: utf-8 -*-
# @Time    : 2017/9/22 15:49
# @Author  : Hua
# @Site    : 
# @File    : SqlModel.py
# @Software: PyCharm
from common.Util import NoAttributeError

class SqlModel(object):
    tableName = None
    sql_columns = None

    @classmethod
    def sql_insert(cls):
        columnList = cls.sql_columns
        columns = ','.join([column[0] for column in columnList])
        placeholders = ','.join(map(lambda x: '?', columnList))
        sql = "insert or replace into {tableName} ({columns}) values ({placeholders});".format(tableName=cls.tableName,
                                                                                               columns=columns,
                                                                                               placeholders=placeholders)
        return sql

    def sql_insert_data(self):
        return tuple(map(lambda x: getattr(self, x[0]) if hasattr(self, x[0]) else None, self.sql_columns))

    @classmethod
    def sql_create(cls):
        columns = cls.sql_columns
        if columns == None:
            raise NoAttributeError(message='do not have attribute sql_columns')
        sql_middle = ','.join([' '.join(column) for column in columns])
        sql = "CREATE TABLE {tableName} ({sql_middle})".format(tableName=cls.tableName, sql_middle=sql_middle)
        return sql
