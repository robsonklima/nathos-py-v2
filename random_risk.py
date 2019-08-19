#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from db_helper import DBHelper


def get_project_by_rand():
    project = DBHelper().fetch(u" SELECT    *"
                               u" FROM 	    projects"
                               u" WHERE     id < 18"
                               u" ORDER BY	rand()"
                               u" LIMIT     1")

    if (len(project)):
        return project[0]

    return None

def get_all_risks():
    return DBHelper().fetch(u'SELECT * FROM risks;')

def update_risk(code, risk_id):
    DBHelper().execute(u"UPDATE risks SET code='%s' WHERE id=%s;" % (code, risk_id))


risks = get_all_risks()

for i, risk in enumerate(risks):
    prj = get_project_by_rand()

    update_risk(prj['code'], risk['id'])