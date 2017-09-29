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
    def _sql_columns(cls):
        return [column[0] for column in cls.sql_columns]

    @classmethod
    def sql_insert_str(cls):
        columns = ','.join(cls._sql_columns())
        placeholders = ','.join(map(lambda x: '?', cls.sql_columns))
        sql = "INSERT or REPLACE INTO {tableName} ({columns}) VALUES ({placeholders})".format(tableName=cls.tableName,
                                                                                              columns=columns,
                                                                                              placeholders=placeholders)
        return sql

    def sql_insert_data(self):
        return tuple(map(lambda x: getattr(self, x[0]) if hasattr(self, x[0]) else None, self.sql_columns))

    @classmethod
    def sql_query(cls, *queryColumns, **queryKeys):
        colums = ','.join(queryColumns) if queryColumns else '*'
        where = ' AND '.join(['{}=?'.format(k) for k in queryKeys.iterkeys()])
        where = 'WHERE ' + where if queryKeys else where
        data = [v for v in queryKeys.itervalues()]
        sql = "SELECT {colums} FROM {tableName} {where}".format(colums=colums, tableName=cls.tableName, where=where)
        return sql, data, queryColumns or cls._sql_columns()

    @classmethod
    def sql_create(cls):
        columns = cls.sql_columns
        if columns == None:
            raise NoAttributeError('do not have attribute sql_columns')
        sql_middle = ','.join([' '.join(column) for column in columns])
        sql = "CREATE TABLE {tableName} ({sql_middle})".format(tableName=cls.tableName, sql_middle=sql_middle)
        return sql
