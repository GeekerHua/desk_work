import sqlite3

from Model.LabelsModel import LabelsModel
from Model.MilestoneModel import MilestoneModel
from Model.SqlModel import SqlModel


class IssueModel(SqlModel):
    milestone = MilestoneModel
    tableName = 'T_Issue'

    sql_columns = [
        ('id', 'INT', 'PRIMARY KEY'),
        ('url', 'TEXT'),
        ('labels_url', 'TEXT'),
        ('comments_url', 'TEXT'),
        ('html_url', 'TEXT'),
        ('number', 'INT'),
        ('title', 'TEXT'),
        ('state', 'TEXT', "DEFAULT 'open'"),
        ('locked', 'BLOB', "DEFAULT FALSE"),
        ('milestone_id', 'INT'),
        ('milestone_no', 'INT'),
        ('body', 'TEXT'),
    ]

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
