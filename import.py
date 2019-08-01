#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import pymysql

try:
    db = pymysql.connect(user='root', password='root', database='nhatos_v2', host='127.0.0.1')

    with db.cursor() as cursor:
        q = u"TRUNCATE TABLE projects;"
        cursor.execute(q)

    db.commit()
    db.close()
except Exception as ex:
    print(ex.message)

df_projects = pd.ExcelFile(u'data/projects.xlsx').parse('projects')

for i, r in df_projects.T.iteritems():
    try:
        db = pymysql.connect(user='root', password='root', database='nhatos_v2', host='127.0.0.1')

        with db.cursor() as cursor:
            q = u"INSERT INTO projects (code, title, description, domain, deadline, end, estimated_hours, hours_done)" \
                u" VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(q, (r['code'], r['title'], r['description'].replace('\r', '').replace('\n', ''),
                               r['domain'], r['deadline'], r['end'], r['estimated_hours'], r['hours_done']))

        db.commit()
        db.close()
    except Exception as ex:
        print(ex.message)


try:
    db = pymysql.connect(user='root', password='root', database='nhatos_v2', host='127.0.0.1')

    with db.cursor() as cursor:
        q = u"TRUNCATE TABLE requirements;"
        cursor.execute(q)

    db.commit()
    db.close()
except Exception as ex:
    print(ex.message)

df_requirements = pd.ExcelFile(u'data/requirements.xlsx').parse('requirements')

for i, r in df_requirements.T.iteritems():
    try:
        db = pymysql.connect(user='root', password='root', database='nhatos_v2', host='127.0.0.1')

        with db.cursor() as cursor:
            q = u"INSERT INTO requirements (code, title, description)" \
                u" VALUES (%s, %s, %s);"
            cursor.execute(q, (r['code'], r['title'], r['description'].replace('\r', '').replace('\n', '')))

        db.commit()
        db.close()
    except Exception as ex:
        print(ex.message)
