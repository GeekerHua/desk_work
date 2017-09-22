# -*- coding: utf-8 -*-
# @Time    : 2017/9/21 15:21
# @Author  : Hua
# @Site    : 
# @File    : IssueManager.py
# @Software: PyCharm
import sqlite3

import DBManager


class IssueManager(object):
    # def __init__(self):
    # self.conn = sqlite3.connect('sql.db')
    # self.conn.text_factory = str
    # self.cursor = conn.cursor()

    @staticmethod
    def updateIssue(issue):
        conn = sqlite3.connect('sql.db')
        conn.text_factory = str
        cursor = conn.cursor()
        tmpdict = issue.__dict__
        (keys, values) = zip(*tmpdict.items())
        key = ','.join(keys)
        value = ','.join(['?' for i in range(len(values))])
        sql = issue.updateSql()
        print sql
        cursor.execute(sql, values)
        cursor.close()
        conn.commit()
        conn.close()

    @staticmethod
    def updaeIssues(issues):
        conn = sqlite3.connect('sql.db')
        conn.text_factory = str
        cursor = conn.cursor()
        for issue in issues:
            # tmpdict = issue.__dict__
            # (keys, values) = zip(*tmpdict.items())
            # key = ','.join(keys)
            # value = ','.join(['?' for i in range(len(values))])
            sql = issue.updateSql()
            print sql
            cursor.execute(sql)
        cursor.close()
        conn.commit()
        conn.close()
