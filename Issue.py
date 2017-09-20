class Issue(object):
    def __init__(self):
        self.repository_url = None
        self.labels_url = None
        self.events_url = None
        self.html_url = None
        self.id = None
        self.number = None
        self.title = None
        self.state = 'open'  # open/closed
        self.body = 'TEXT'
        self.locked = False
        self.url = 'TEXT'

        self.labels = [LabelsModel]
        self.milestone = MilestoneModel
        self.assignee_id = 'INTEGER'

    @classmethod
    def getCreateSql(cls):
        keysDict = cls().__dict__
        tmpSql = ','.join(['"{k}" {v}'.format(k=k, v=v) for k, v in keysDict.items()])
        return 'CREATE TABLE  if not exists "T_issues" (' + tmpSql + ',PRIMARY KEY("id"))'


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
