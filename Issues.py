# -*- coding: utf-8 -*-
import json
import urllib2
import sqlite3
import DBManager
from Issue import Issue
REPO_ID = 60256158
ACCESS_TOKEN = "e29c52830150eef17d5ac38dc7eedb2ae3dd4433b7604e62c4a9e56a9b90706910d0916f52fad370"

class IssueManager(object):
    # def __init__(self):
        # self.conn = sqlite3.connect('sql.db')
        # self.conn.text_factory = str
        # self.cursor = conn.cursor()

    def updateIssue(self, issue):
        DBManager.createDB()
        conn = sqlite3.connect('sql.db')
        conn.text_factory = str
        cursor = conn.cursor()
        tmpdict = issue.__dict__
        (keys, values) = zip(*tmpdict.items())
        key = ','.join(keys)
        value = ','.join(['?' for i in range(len(values))])
        sql = 'insert or replace into T_issues (%s) values (%s)'%(key, value)
        # print tmpdict.items()
        cursor.execute(sql, values)
        cursor.close()
        conn.commit()
        conn.close()

    def getResponse(self):
        # url = "https://api.zenhub.io/p1/repositories/{REPO_ID}/epics".format(
            # REPO_ID=REPO_ID)
        url = "https://api.github.com/repos/geekerhua/geekerhua.github.io/issues"

        querystring = {"access_token": ACCESS_TOKEN}
        headers = {"Authorization": "Basic R2Vla2VySHVhOjE0MTU5MjZHZWVrZXJHaXRIdWI="}
        url = url + '?' + '&'.join(['{k}={v}'.format(k=k, v=v)
                                    for k, v in querystring.items()])
        request = urllib2.Request(url, headers=headers)
        return urllib2.urlopen(request)

    def getIssueList(self):
        # 1.先查数据库
        conn = sqlite3.connect('sql.db')
        conn.text_factory = str
        cursor = conn.cursor()
        keys = Issue().__dict__.keys()
        result = cursor.execute('select {keys} from T_issues'.format(keys=keys))
        print result.fetchone()
        # 2.数据库没有再去请求，放到异步去
        # datas = json.loads(getResponse().read())
        return result

    def getIssue(self, number):
        issue = Issue()
        # 1.先查数据库

        # 2.数据库没有再去请求

        return issue

def main():
    manager = IssueManager()
    datas = manager.getIssueList()
    # tmpList = []
    # for data in datas:
    #     issue = Issue()
    #     issue.id = data['id']
    #     issue.number = data['number']
    #     issue.title = data['title'].encode('utf-8')
    #     issue.body = data['body'].encode('utf-8')
    #     issue.url = data['url'].encode('utf-8')
    #     issue.pipeline = ''  # data['pipeline']
    #     issue.state = data['state'].encode('utf-8')
    #     issue.assignees_id = 0
    #     issue.assignee_id = 0
    #     issue.milestone_id = data.get('milestone', {}).get('id', 0)
    #     updateIssue(issue)
    #     tmpList.append({
    #         "valid": True,
    #         "title": '#' + str(issue.number) + ' ' + issue.title,
    #         "subtitle": issue.body,
    #         # "icon": {"path": icon},
    #         "arg": str(issue.number),
    #         "mods": {
    #             "cmd": {
    #                 "valid": True,
    #                 "arg": issue.url,
    #                 "subtitle": "open url in default browser"
    #             },
    #         },
    #     })
    # ret = json.dumps({"items": tmpList})
    # print ret


if __name__ == '__main__':
    main()
