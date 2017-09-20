#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# 2017-09-19 15:39:29
"""

__author__ = 'geekerhua@sina.com'

import json, urllib2, ModelTools, os
from Issue import Issue

GitHub_Authorization = os.getenv('GitHub_Authorization')
Repo_Name = os.getenv('Repo_Name')
Owner_name = os.getenv('GeekerHua')
Base_Api = "https://api.github.com"


class RESTful(object):
    GET = 'GET'
    POST = 'POST'
    PATCH = 'PATCH'


class Repo(object):
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.owner = Owner_name

    def getAllIssues(self):
        resp = requestApi(renderUrl("/repos/:owner/:repo/issues", repo=self.name, owner=self.owner))
        if resp.code == 200:
            return json.loads(resp.read())
        else:
            return None

    def repoInfo(self):
        resp = requestApi(renderUrl('/repos/:owner/:repo', repo=self.name, owner=self.owner))
        return resp

    def createIssue(self, issue):
        """
        创建新的issue
        :type issue: Issue
        :rtype: response
        """
        data = {
            "title": issue.title,
            "body": issue.body,
            "assignees": [self.owner],
            "milestone": issue.milestone_id,
            "labels": issue.labels_name  # 这个labels_name需要改成label name 字符串组成的list
        }
        formData = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        resp = requestApi(renderUrl("/:repo/issues", repo=self.name), method=RESTful.POST, data=formData,
                          headers=headers)
        return resp

    def editeIssue(self, issue):
        """
        修改issue
        :type issue: Issue
        :rtype: response
        """
        data = {
            "title": issue.title,
            "body": issue.body,
            "assignees": [self.owner],
            "milestone": issue.milestone_id,
            "state": issue.state,
            "labels": issue.labels_name  # 这个labels_name需要改成label name 字符串组成的list
        }
        formData = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        resp = requestApi(renderUrl('/repos/:owner/:repo/issues/:number', repo=self.name, issue_no=issue.number),
                          method=RESTful.PATCH,
                          data=formData, headers=headers)
        return resp


def renderUrl(api, **kwargs):
    for k, v in kwargs.iteritems():
        api = api.replace(':' + k, v, 1)
    url = Base_Api + api
    return url


def requestApi(url, method=RESTful.GET, data=None, headers={}):
    """

    :rtype: response.
    """
    defaultHeaders = {"Authorization": GitHub_Authorization}
    headers.update(defaultHeaders)
    request = urllib2.Request(url, headers=headers, data=data)
    request.get_method = lambda: method
    try:
        return urllib2.urlopen(request)
    except urllib2.HTTPError as e:
        # TODO: 处理不同的code if e.code == 400:
        print e, request.get_method(), url, headers, data
        return None


def main():
    repo = Repo(Repo_Name, None)

    result = repo.getAllIssues()
    if result:
        r = ModelTools.toModel(result, Issue)
        print r


if __name__ == '__main__':
    main()
