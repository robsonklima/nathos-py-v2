#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import time
from db_helper import DBHelper


def get_all_projects():
    return DBHelper().fetch(u'SELECT * FROM projects;')

def update_project(project_id):
    DBHelper().execute(u"UPDATE projects SET size='%s' WHERE id=%s;" %
                       (random.choice(['SMALL', 'SMALL', 'STANDARD', 'STANDARD', 'STANDARD', 'LARGE']), project_id))



projects = get_all_projects()

for i, prj in enumerate(projects):
    try:
        update_project(prj['id'])
        #print(random.choice(['SMALL', 'STANDARD', 'LARGE']))
    except Exception as ex:
        print(ex)