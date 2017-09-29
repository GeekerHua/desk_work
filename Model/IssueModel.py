from GHTools.DBManager import execSQL
from Model.LabelsModel import LabelsModel
from Model.MilestoneModel import MilestoneModel
from Model.SqlModel import SqlModel
from common.Util import SQLAction


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

    def __init__(self, title=None, body=None):
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
        self.milestone = MilestoneModel
        self.assignee_id = 'INTEGER'

    def oppositeState(self):
        return 'open' if self.state == 'closed' else 'closed'

    # def __repr__(self):
    #     return vars(self)

    @staticmethod
    @execSQL(SQLAction.executemany)
    def updaeIssues(issues):
        result = IssueModel.sql_insert_str(), [issue.sql_insert_data() for issue in issues]
        return result

    @classmethod
    @execSQL(SQLAction.queryAll)
    def queryIssues(cls, *queryColumns, **queryKeys):
        return IssueModel.sql_query(*queryColumns, **queryKeys)

    @property
    def labelsList(self):
        return []  # [item.name for item in self.labels]

    def alfredItem(self):
        toState = 'close' if self.state == 'open' else 'open'
        icon = self.state
        return {
            "valid": True,
            "title": self.title,
            "subtitle": self.body,
            "quicklookurl": self.body,  # self.html_url,
            "arg": self.id,
            "autocomplete": self.title,
            "icon": {
                "path": "./icon/{}.png".format(icon)
            },
            "mods": {
                "cmd": {
                    "valid": True,
                    "arg": self.id,
                    "subtitle": "{} this issue".format(toState)
                },
            },
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
