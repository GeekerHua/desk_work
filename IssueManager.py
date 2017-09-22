# -*- coding: utf-8 -*-
# @Time    : 2017/9/21 15:21
# @Author  : Hua
# @Site    : 
# @File    : IssueManager.py
# @Software: PyCharm
import sqlite3

import DBManager
from Model.IssueModel import IssueModel
from common.Util import SQLAction


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
        sql, args = issue.sql_insert_data()
        cursor.execute(sql, args)
        cursor.close()
        conn.commit()
        conn.close()

    @staticmethod
    @DBManager.execSQL(SQLAction.executemany)
    def updaeIssues(issues):
        return IssueModel.sql_insert(), (issue.sql_insert_data() for issue in issues)
