#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import time
from db_helper import DBHelper


def strTimeProp(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))

def randomDate(start, end):
    return strTimeProp(start, end, '%Y-%m-%d %H:%M:%S', random.random())

def get_all_projects():
    return DBHelper().fetch(u'SELECT * FROM projects;')

def get_all_requirements():
    return DBHelper().fetch(u'SELECT * FROM requirements;')

def update_project(project_id):
    DBHelper().execute(
        u"UPDATE projects SET added='%s' WHERE id=%s;"
        % randomDate(u"2017-01-01 00:00:01", u"2017-10-30 23:59:59"), p['id'])

def update_requirement(requirement_id):
    DBHelper().execute(
        u"UPDATE requirements SET added='%s' WHERE id=%s;"
        % randomDate(u"2017-01-01 00:00:01", u"2017-10-30 23:59:59"), p['id'])


projects = get_all_projects()

for i, p in enumerate(projects):
    update_project(p['id'])

requirements = get_all_requirements()

for i, r in enumerate(requirements):
    update_requirement(r['id'])
