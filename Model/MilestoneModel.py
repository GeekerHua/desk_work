# -*- coding: utf-8 -*-
# @Time    : 2017/9/22 15:50
# @Author  : Hua
# @Site    : 
# @File    : MilestoneModel.py
# @Software: PyCharm
from Model.SqlModel import SqlModel


class MilestoneModel(SqlModel):
    tableName = 'T_Milestone'
    sql_columns = [
        ('id', 'INT PRIMARY KEY'),
        ('url', 'TEXT'),
        ('html_url', 'TEXT'),
        ('labels_url', 'TEXT'),
        ('number', 'INT'),
        ('title', 'TEXT'),
        ('description', 'TEXT'),
        ('open_issues', 'INT'),
        ('close_issues', 'INT'),
        ('state', "TEXT DEFAULT 'open'"),
        ('create_at TEXT'),
        ('updated_at', 'TEXT')
    ]

    def __init__(self):
        self.url = None
        self.html_url = None
        self.labels_url = None
        self.id = None
        self.number = None
        self.title = None
        self.description = None
        self.open_issues = None
        self.closed_issues = None
        self.state = None
        self.created_at = None
        self.updated_at = None
        self.due_on = None
        self.closed_at = None
