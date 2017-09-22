# -*- coding: utf-8 -*-
import json
import urllib2

REPO_ID =
ACCESS_TOKEN = ""

def getResponse():
    url = "https://api.zenhub.io/p1/repositories/{REPO_ID}/epics".format(
        REPO_ID=REPO_ID)
    querystring = {"access_token": ACCESS_TOKEN}
    url = url + '?' + '&'.join(['{k}={v}'.format(k=k, v=v) for k,v in querystring.items()])
    request = urllib2.Request(url)
    return urllib2.urlopen(request)

def getTitle(issue_number):
    # 从数据库查,如果没有，发送请求，从网络获取，然后保存到数据库，并返回

def main():
    datas = json.loads(getResponse().read())

    tmpList = []
    for data in datas.get('epic_issues', []):
        issue_number = data['issue_number']
        title = getTitle(issue_number)
        tmpList.append({
                    "valid": True,
                    "title": '#' + str(issue_number) + title,
                    "subtitle": "", 
                    # "icon": {"path": icon},
                    "arg": str(issue_number),
                    "mods": {
                        "cmd": {
                            "valid": True,
                            "arg": data['issue_url'],
                            "subtitle": "open url in default browser"
                        },
                    },
                })
    ret = json.dumps({"items": tmpList})
    print ret
    
if __name__ == '__main__':
    main()
