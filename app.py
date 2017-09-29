#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# 2017-09-19 15:39:29
__author__ = 'geekerhua@sina.com'
"""
import argparse
import json
import logging

from GHTools import ModelTools
from GHTools.DBManager import DB
from Model.IssueModel import IssueModel
from Model.LabelsModel import LabelsModel
from Model.MilestoneModel import MilestoneModel
from Model.Repo import Repo
from common.Util import NoRepoError


def refreshAllIssues(repoName):
    repo = Repo(repoName)
    repo.getAllISSuesFromNet()

def getAllIssues(repoName):
    repo = Repo(repoName)
    issueData = repo.getAllIssues()
    if issueData:
        logging.debug('Start generate alfred data %s', str(issueData))
        if isinstance(issueData, list):
            items = [item.alfredItem() for item in issueData]
        else:
            items = issueData.alfredItem()
        return json.dumps({"items": items})


def addIssue(repoName, title, body=None):
    issue = IssueModel(title, body)
    issue.milestone = MilestoneModel()
    repo = Repo(repoName)
    result = repo.addIssue(issue)
    if result:
        return 0


def editIssue(repoName, issueNo, title, body=None):
    issue = IssueModel(title, body)
    issue.milestone = MilestoneModel()
    issue.number = issueNo
    repo = Repo(repoName)
    result = repo.editIssue(issue)
    if result:
        # 成功了，保存到数据库，替换旧数据。
        return 0

def changeIssueState(issueId, repoName):
    repo = Repo(repoName)
    issue = repo.queryIssue(issueId)
    issue.state = issue.oppositeState()
    issue.milestone = MilestoneModel()
    result = repo.editIssue(issue)
    print result
    if result:
        IssueModel.updaeIssues([issue])
        return 0


if __name__ == '__main__':

    logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(message)s')
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
    parser_b.add_argument('-s', '--source', type=str, help='source of issues: net/db')

    parser_d = subparsers.add_parser('issue', help='contral issue')
    parser_d.add_argument('-m', '--mode', type=str, help='mode of the issue,detail/state')
    parser_d.add_argument('-r', '--repo', type=str, help='select a repo')
    parser_d.add_argument('-i', '--id', type=int, help='the id of the issue')

    args = parser.parse_args()
    # print vars(args)
    # exit(0)

    # 需要保存miliestone和Label，

    # 先支持 repo(name)， title， body
    # add: python app.py add add -t title -b body
    # edit: python app.py edit edit -n 15 -s open -t title -b body
    # list: python app.py list list -r ropo -a true
    DB.createTables(IssueModel, LabelsModel, MilestoneModel)
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
            raise NoRepoError('must have repo and title')
    elif args.action == 'list':
        repo = args.repo
        source = args.source
        if repo:
            logging.info('Start get all issues from repo %s', repo)
            if source == 'db':
                print(getAllIssues(repo))
            elif source == 'net':
                refreshAllIssues(repo)
        else:
            raise NoRepoError('must have repo')
    elif args.action == 'issue':
        repoName = args.repo
        issueId = args.id
        mode = args.mode
        if mode == 'state':
            changeIssueState(issueId, repoName)
    else:
        print('do not suppost thid action:{}'.format(args.action))
