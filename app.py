#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# 2017-09-19 15:39:29
"""

__author__ = 'geekerhua@sina.com'

import argparse
import json
import os
import urllib2

from GHTools import ModelTools
from Issue import Issue, MilestoneModel

GitHub_Authorization = os.getenv('GitHub_Authorization')
Repo_Name = os.getenv('Repo_Name')
Owner_name = os.getenv('Owner_name')
Base_Api = "https://api.github.com"


class RESTful(object):
    GET = 'GET'
    POST = 'POST'
    PATCH = 'PATCH'


class Repo(object):
    def __init__(self, name=None, id=None):
        self.name = name
        self.id = id
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
        :type issue: Issue
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
        :type issue: Issue
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


def getAllIssues(repoName):
    repo = Repo(repoName)
    result = repo.getAllIssues()
    if result:
        r = ModelTools.toModel(result, Issue)
        items = [item.alfredItem() for item in r]
        return json.dumps({"items": items})


def addIssue(repoName, title, body=None):
    issue = Issue(title, body, MilestoneModel())
    repo = Repo(repoName)
    result = repo.addIssue(issue)
    if result:
        return 0


def editIssue(repoName, issueNo, title, body=None):
    issue = Issue(title, body, MilestoneModel())
    issue.number = issueNo
    repo = Repo(repoName)
    result = repo.editIssue(issue)
    if result:
        # 成功了，保存到数据库，替换旧数据。
        return 0


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('action', help='action help')
    subparsers = parser.add_subparsers(help='sub-command help')

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('-r', '--repo', type=str, help='select a repo')
    parent_parser.add_argument('-t', '--title', type=str, help='issue title')
    parent_parser.add_argument('-b', '--body', type=str, help='issue body')
    parent_parser.add_argument('-m', '--milestone', type=int, help='issue milestone')
    parent_parser.add_argument('-l', '--labels', nargs='+', type=str, help='issue labels')

    parser_a = subparsers.add_parser('add', help='add issue help', parents=[parent_parser])  # 传递多个参数

    parser_c = subparsers.add_parser('edit', help='edit issue help', parents=[parent_parser])
    parser_c.add_argument('-s', '--state', help='issue state')
    parser_c.add_argument('-n', '--issue_no', help='issue number')

    parser_b = subparsers.add_parser('list', help='list all issue help')
    # parser_b.add_argument('-l', '--list', help='list all issues')
    parser_b.add_argument('-r', '--repo', type=str, help='select a repo')
    parser_b.add_argument('-a', '--all', type=bool, help='all issue inclue closed')

    args = parser.parse_args()
    # print vars(args)
    # exit(0)

    # 需要保存miliestone和Label，

    # 先支持 repo(name)， title， body
    # add: python app.py add add -t title -b body
    # edit: python app.py edit edit -n 15 -s open -t title -b body
    # list: python app.py list list -r ropo -a true
    if args.action in ['add', 'edit']:
        repo = args.repo
        title = args.title
        body = args.body
        mileston = args.milestone
        labels = args.labels
        issueNo = args.issue_no
        if repo and title:
            if args.action == 'add':
                print(addIssue(repo, title, body))
            else:  # edit
                print(editIssue(repo, issueNo, title, body))
        else:
            print('must have repo and title')
    elif args.action == 'list':
        repo = args.repo
        if repo:
            print(getAllIssues(repo))
        else:
            print('must have repo')
    else:
        print('do not suppost thid action:{}'.format(args.action))
