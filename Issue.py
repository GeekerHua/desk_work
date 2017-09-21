class LabelsModel(object):
    def __init__(self):
        self.id = None
        self.url = None
        self.name = None
        self.color = None
        self.default = None


class MilestoneModel(object):
    def __init__(self):
        self.url = None
        self.html_url = None
        self.labels_url = None
        self.id = None
        self.number = None
        self.title = None
        self.description = None
        self.open_issues = None
        self.closed_issues = None
        self.state = None
        self.created_at = None
        self.updated_at = None
        self.due_on = None
        self.closed_at = None


class Issue(object):
    milestone = MilestoneModel

    def __init__(self, title=None, body=None, milestone=MilestoneModel, labels=[LabelsModel], state='open'):
        self.repository_url = None
        self.labels_url = None
        self.events_url = None
        self.html_url = None
        self.id = None
        self.number = None
        self.title = title
        self.state = 'open'  # open/closed
        self.body = body
        self.locked = False
        self.url = 'TEXT'

        self.labels = [LabelsModel]
        self.milestone = milestone
        self.assignee_id = 'INTEGER'

    @property
    def labelsList(self):
        return []  # [item.name for item in self.labels]

    def alfredItem(self):
        return {
            "valid": True,
            "title": self.title,
            "subtitle": self.body,
            "quicklookurl": self.body,  # self.html_url,
            "arg": self.number,
            "autocomplete": self.title
        }

    @classmethod
    def getCreateSql(cls):
        keysDict = cls().__dict__
        tmpSql = ','.join(['"{k}" {v}'.format(k=k, v=v) for k, v in keysDict.items()])
        return 'CREATE TABLE  if not exists "T_issues" (' + tmpSql + ',PRIMARY KEY("id"))'

    def openIssue(self):
        pass

    def closeIssue(self):
        pass

    def deailIssue(self):
        return [
            {
                "valid": True,
                "title": 'close',
                "subtitle": 'close the issue',
                "arg": 'close'
                # "autocomplete": self.title
            },
            {
                "valid": True,
                "title": 'commit',
                "subtitle": 'list commit of this issue',
                "arg": 'commit'
            },
            {
                "valid": True,
                "title": 'milestone',
                "subtitle": 'list milestone of this issue',
                # "quicklookurl": self.body,  # self.html_url,
                "arg": 'milestone'
            },
            {
                "valid": True,
                "title": 'label',
                "subtitle": 'list labels of this issue',
                # "quicklookurl": self.body,  # self.html_url,
                "arg": 'label'
            }
        ]
