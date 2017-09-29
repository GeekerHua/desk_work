# coding=utf-8
import sqlite3

import logging

# from Model import LabelsModel
# from Model.IssueModel import IssueModel
# from Model.MilestoneModel import MilestoneModel
import types

from Model.SqlModel import SqlModel
from common.Util import SQLAction, WrapperMethodError


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
                    sqlstr, datas = func(*args, **kwargs)
                    logging.debug('Start update sql %s data = %s', sqlstr, str(list(datas)))
                    cursor.executemany(sqlstr, datas)
                    logging.info('exec sql success')
                elif action == SQLAction.queryAll:
                    sqlstr, datas, colums = func(*args, **kwargs)
                    clsM = args[0]
                    if not issubclass(clsM, SqlModel):
                        raise WrapperMethodError('this wrapper must use classmethod, {}'.format(str(type(clsM))))
                    logging.debug('Start execute sql %s data = %s', sqlstr, str(list(datas)))
                    cursor.execute(sqlstr, datas)
                    logging.info('exec sql success')
                    result = cursor.fetchall()
                    if colums:
                        ls = []
                        for item in result:
                            model = clsM()
                            for k, v in zip(colums, item):
                                setattr(model, k, v)
                            ls.append(model)
                        return ls
                    else:
                        return result
                conn.commit()
            return 0

        return wrapper

    return decorator


class DB(object):
    @staticmethod
    def detectionTable(tableName, cursor):
        return \
            cursor.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='%s';" % tableName).fetchone()[0]

    @staticmethod
    @execSQL(SQLAction.create)
    def createTables(*args):
        return [(modelCls.tableName, modelCls.sql_create()) for modelCls in args]

    # if __name__ == '__main__':
    # print DB.createTables(IssueModel, LabelsModel, MilestoneModel)
