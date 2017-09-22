# -*- coding: utf-8 -*-
# @Time    : 2017/9/21 15:02
# @Author  : Hua
# @Site    : 
# @File    : Repo.py
# @Software: PyCharm

import json
import os

from Model.IssueModel import IssueModel
from common.NetManager import renderUrl, requestApi
from common.Util import RESTful

Repo_Name = os.getenv('Repo_Name')
Owner_name = os.getenv('Owner_name')


class Repo(object):
    def __init__(self, name=None, ID=None):
        self.name = name
        self.id = ID
        self.owner = Owner_name

    def getAllIssues(self):
        resp = requestApi(renderUrl("/repos/:owner/:repo/issues", repo=self.name, owner=self.owner))
        if resp.code == 200:
            return resp.read()
        else:
            return None

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
