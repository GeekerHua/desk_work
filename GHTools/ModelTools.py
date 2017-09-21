# -*- coding: utf-8 -*-
# @Time    : 2017/9/20 10:36
# @Author  : Hua
# @Site    : 
# @File    : ModelDict.py.py
# @Software: PyCharm
import importlib
import json
import sys

BASE_TYPE_LIST = [int, unicode, str, bool, tuple, float]

ll = {
    "b1": 'is b1',
    "b2": 3,
    "b3": True,
    "d": [2, 3, 5]
}

jj = {
    # "a": 'is a ',
    "b": [
        {
            "b1": 'is b1',
            "b2": 3,
            "b3": True,
            "d": [2, 3, 5]
        }
    ],
    "c": {
        "b1": 'is b1',
        "b2": 3,
        "b3": True,
        "d": [2, 3, 5, 889]
    },
    "cc": 'dd'
}

j = [
    {
        "a": 'is a ',
        "b": [
            {
                "b1": 'is b1',
                "b2": 3,
                "b3": True,
                "d": [2, 3, 5]
            },
            {
                "b1": 'is b1',
                "b2": 3,
                "b3": True,
                "d": [2, 3, 5, 889]
            }
        ],
        "c": {
            "b1": 'is b1',
            "b2": 3,
            "b3": True
        },
        "cc": 'dd'
    },
    {
        "a": 'is a ',
        "b": [
            {
                "b1": 'is b1',
                "b2": 3,
                "b3": True
            },
            {
                "b1": 'is b1',
                "b2": 3,
                "b3": True
            }
        ],
        "c": {
            "b1": 'is b1',
            "b2": 3,
            "b3": True
        }
    }
]


class ReflectTool(object):
    @staticmethod
    def _getPackageAndClassName(fullName):
        """
        获取module名字和class name
        :type fullName: str
        :rtype: tuple[str,str]
        """
        pos = fullName.rfind('.')
        moduleName = fullName[:pos]
        className = fullName[pos + 1:]
        return moduleName, className

    @staticmethod
    def dynamicNewObj(moduleClassName, *args, **kwargs):
        """
        动态new 对象
        :type moduleClassName: str
        :rtype: object
        """
        moduleName, className = ReflectTool._getPackageAndClassName(moduleClassName)
        if (not sys.modules.has_key(moduleName)):
            targetModule = importlib.import_module(moduleName)
        else:
            targetModule = sys.modules.get(moduleName)
        targetClass = getattr(targetModule, className)
        return targetClass(*args, **kwargs)
        # def __init__(self):
        # self.message = 'list Model must have key'


class C(object):
    def __init__(self):
        self.b1 = None
        self.b2 = None
        self.b3 = None
        self.d = []


class B(object):
    pass


class A(object):
    # b = B
    def __init__(self):
        self.a = None
        self.b = [C]
        # self.c = C


class ModelError(Exception):
    pass


def toModel(data, clsType):
    """
    将dict、json转成model
    :rtype: object
    """
    if isinstance(data, basestring):  # json
        data = toDict(data)
    return dict2Model(data, clsType)


def toDict(data):
    """
    将model，json转成dict或者list
    :rtype: list[Any] | dict[str,Any]
    """
    if isinstance(data, basestring):  # json
        return json.loads(data)
    else:  # model
        return model2Dict(data)


def toJson(data):
    """
    将model，dict，list转成json
    :rtype: json
    """
    if type(data) in [list, dict]:  # dict
        data = json.loads(data)
    elif isinstance(data, object):  # model
        data = toJson(model2Dict(data))
    return data


    # TODO : 处理类对应哪个属性缺失的情况。


def dict2Model(data, clsType=None, key=None):
    """
    :type data: object | list[Any]| dict[str, str|object]
    :type clsType: class
    :rtype: A | list[A]
    """
    if type(data) in BASE_TYPE_LIST:
        return data
    elif isinstance(data, list):
        if key and hasattr(clsType(), key):
            if getattr(clsType(), key):  # [object]
                tmpCls = getattr(clsType(), key)[0]
            else:  # [baseType]
                return data
        else:  # [dict]
            tmpCls = clsType
        return [dict2Model(item, tmpCls, None) for item in data]
    elif isinstance(data, dict):
        # if key and hasattr(clsType(), key):
        tmpCls = getattr(clsType, key) if key else clsType
        m = tmpCls()
        for key, v in data.iteritems():
            if key in m.__dict__:
                setattr(m, key, dict2Model(v, tmpCls, key))
        return m
    else:
        return data


def model2Dict(data):
    """

    :type data: list[object] | object | dict[str, str|object]
    :rtype: list[Any] | dict[str, Any]
    """
    if type(data) in BASE_TYPE_LIST or data == None:
        return data
    elif isinstance(data, list):
        return [model2Dict(item) for item in data]
    elif isinstance(data, object):
        dic = data.__dict__
        dic.update({k: model2Dict(v) for k, v in dic.iteritems() if v != None})
        return dic
    else:
        return data


if __name__ == '__main__':
    # print getattr(A(), 'c')
    # print A().__dict__
    # print A.__dict__
    a = toModel(jj, A)
    # a = dict2Model(ll, C)
    b = toDict(a)
    print '****'
    print a
    print b

    # print type(A().b)
    # print A().c().__dict__
