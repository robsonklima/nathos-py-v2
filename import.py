#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
from db_helper import DBHelper


DBHelper().execute(u"TRUNCATE TABLE projects;")

df_projects = pd.ExcelFile(u'data/projects.xlsx').parse('projects')
for i, p in df_projects.T.iteritems():
    DBHelper().execute(u"INSERT INTO projects (code, title, description, domain, deadline, "
                       u"end, estimated_hours, hours_done)"
                       u"VALUES ('%s', '%s', '%s', '%s', '%s', '%s', %s, %s);" %
                       (p['code'], p['title'], p['description'].replace('\r', '').replace('\n', ''),
                       p['domain'], p['deadline'], p['end'], p['estimated_hours'], p['hours_done']))


DBHelper().execute(u"TRUNCATE TABLE requirements;")

df_requirements = pd.ExcelFile(u'data/requirements.xlsx').parse('requirements')
for i, r in df_projects.T.iteritems():
    DBHelper().execute(u"INSERT INTO requirements (code, title, description)"
                       u"VALUES ('%s', '%s', '%s', '%s', '%s', '%s', %s, %s);" %
                       (r['code'], r['title'], r['description'].replace('\r', '').replace('\n', '')))
