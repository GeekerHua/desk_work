# coding=utf-8
import sqlite3

T_IssueSql = """
CREATE TABLE T_Issue  \
(
    id INT PRIMARY KEY,
    url TEXT,
    labels_url TEXT,
    comments_url TEXT,
    html_url TEXT,
    number INT,
    title TEXT,
    state TEXT DEFAULT 'open',
    locked BLOB DEFAULT FALSE,
    milestone_id INT,
    milestone_no INT,
    body TEXT
)
"""

T_LabelSql = """
CREATE TABLE T_label \
(
    id INT PRIMARY KEY,
    url TEXT,
    name TEXT,
    color TEXT,
    "default" BLOB DEFAULT FALSE
)
"""

T_MilestoneSql = """
CREATE TABLE T_Milestone  \
(
    id INT PRIMARY KEY,
    url TEXT,
    html_url TEXT,
    labels_url TEXT,
    number INT,
    title TEXT,
    description TEXT,
    open_issues INT,
    close_issues INT,
    state TEXT DEFAULT 'open',
    create_at TEXT,
    updated_at TEXT
)
"""

def detectionTable(tableName, conn):
    return conn.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='%s';" % tableName).fetchone()[
        0]


def createDB():
    conn = sqlite3.connect('sql.db')
    conn.text_factory = str
    c = conn.cursor()
    if not detectionTable('T_Issue', conn):
        c.execute(T_IssueSql)
    if not detectionTable('T_Label', conn):
        c.execute(T_LabelSql)
    if not detectionTable('T_Milestone', conn):
        c.execute(T_MilestoneSql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    createDB()
