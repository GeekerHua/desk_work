# coding=utf-8
import sqlite3

from Model import LabelsModel
from Model.IssueModel import IssueModel
from Model.MilestoneModel import MilestoneModel
from common.Util import SQLAction


def execSQL(action=SQLAction.execute):
    def decorator(func):
        def wrapper(*args, **kwargs):
            with sqlite3.connect('sql.db') as conn:
                conn.text_factory = str
                cursor = conn.cursor()
                if action == SQLAction.create:
                    for tableName, sqlstr in func(*args, **kwargs):
                        if not DB.detectionTable(tableName, cursor):
                            cursor.execute(sqlstr)
                elif action == SQLAction.executemany:
                    sql, datas = func(*args, **kwargs)
                    print datas.next()
                    cursor.executemany(sql, datas)
                conn.commit()
            return 0

        return wrapper

    return decorator


class DB(object):
    @staticmethod
    def detectionTable(tableName, cursor):
        return \
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='%s';" % tableName).fetchone()[0]

    @staticmethod
    @execSQL(SQLAction.create)
    def createTables(*args):
        return [(modelCls.tableName, modelCls.sql_create()) for modelCls in args]


if __name__ == '__main__':
    print DB.createTables(IssueModel, LabelsModel, MilestoneModel)
