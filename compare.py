#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import time
from db_helper import DBHelper


def get_all_projects():
    return DBHelper().fetch(u'SELECT * FROM projects;')

def get_project(id):
    return DBHelper().fetch(u"SELECT * FROM projects WHERE id=%s;" % (id))

def get_requirements(code):
    return DBHelper().fetch(u"SELECT * FROM requirements WHERE code='%s';" % (code))


projects = get_all_projects()
for i, p in enumerate(projects):
    print(p['id'])

requirements = get_requirements('var2077P')
for i, r in enumerate(requirements):
    print(r['id'])

print(get_project(112))
