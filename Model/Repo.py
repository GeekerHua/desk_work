# -*- coding: utf-8 -*-
# @Time    : 2017/9/21 15:02
# @Author  : Hua
# @Site    : 
# @File    : Repo.py
# @Software: PyCharm

import json
import os
import threading
from multiprocessing import Process
from GHTools import ModelTools
from Model.IssueModel import IssueModel
from common.NetManager import renderUrl, requestApi
from common.Util import RESTful
import logging

Repo_Name = os.getenv('Repo_Name')
Owner_name = os.getenv('Owner_name')


class Repo(object):
    def __init__(self, name=None, ID=None):
        self.name = name
        self.id = ID
        self.owner = Owner_name

    def getAllIssuesFromDB(self):
        logging.info('Start get all Issues from DB')
        result = IssueModel.queryIssues()
        if result:
            return result

    def getAllISSuesFromNet(self):
        logging.info('Start request and refresh all Issues ')
        resp = requestApi(renderUrl("/repos/:owner/:repo/issues", params={'state': 'all'}, repo=self.name, owner=self.owner))
        if resp.code == 200:
            result = resp.read()
            issueData = ModelTools.toModel(result, IssueModel)
            IssueModel.updaeIssues(issueData)
            return issueData
        else:
            logging.warning('request and refresh all Issues failed code = %d, message = ', resp.code, resp.message)
            return None

    def getAllIssues(self):
        # 先从db获取，再从网络获取。
        result = self.getAllIssuesFromDB()
        # p = Process(target=self.getAllISSuesFromNet)
        # p.start()
        # p.join()  # 不需要等待子进程结束，也不行，还是会等待，否则会直接报错。

        ## ====== 多线程，有问题，只有子线程执行完毕，程序才能结束，这时候print的结果才会显示在Alfred中，实际上不需要等待子线程，因此换成进程
        # t = threading.Thread(target=self.getAllISSuesFromNet)
        # t.start()
        ## ====== 多线程 end

        issueData = ModelTools.toModel(result, IssueModel)
        IssueModel.updaeIssues(issueData)
        return issueData

    def queryIssue(self, issueId):
        """

        :rtype: IssueModel
        """
        result = IssueModel.queryIssues(id=issueId)
        if result:
            return result[0]

    def repoInfo(self):
        resp = requestApi(renderUrl('/repos/:owner/:repo', repo=self.name, owner=self.owner))
        return resp

    def addIssue(self, issue):
        """
        创建新的issue
        :type issue: IssueModel
        :rtype: response
        """
        data = {
            "title": issue.title,
            "body": issue.body,
            "assignees": [self.owner],
            "milestone": issue.milestone.id,
            "labels": issue.labelsList
        }
        formData = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        resp = requestApi(renderUrl("/:repo/issues", repo=self.name), method=RESTful.POST, data=formData,
                          headers=headers)
        return resp.read()

    def editIssue(self, issue):
        """
        修改issue
        :type issue: IssueModel
        :rtype: response
        """
        data = {
            "title": issue.title,
            "body": issue.body,
            "assignees": [self.owner],
            "milestone": issue.milestone.id,
            "state": issue.state,
            "labels": issue.labelsList
        }
        formData = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        resp = requestApi(
            renderUrl('/repos/:owner/:repo/issues/:number', repo=self.name, number=issue.number, owner=Owner_name),
            method=RESTful.PATCH,
            data=formData, headers=headers)
        return resp.read()

    def detailIssue(self, issueNo):
        # TODO: 先把issue保存到数据库中
        pass
