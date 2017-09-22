# -*- coding: utf-8 -*-
# @Time    : 2017/9/22 15:50
# @Author  : Hua
# @Site    : 
# @File    : LabelsModel.py
# @Software: PyCharm
from Model.SqlModel import SqlModel


class LabelsModel(SqlModel):
    tableName = 'T_Label'
    sql_columns = [
        ('id', 'INT', 'PRIMARY KEY'),
        ('url', 'TEXT'),
        ('name', 'TEXT'),
        ('color', 'TEXT'),
        ('"default"', 'BLOB', 'DEFAULT FALSE')
    ]

    def __init__(self):
        self.id = None
        self.url = None
        self.name = None
        self.color = None
        self.default = None
