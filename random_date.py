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


projects = DBHelper().fetch(u'SELECT * FROM projects;')

for i, p in enumerate(projects):
    DBHelper().execute(u"UPDATE projects SET added='%s' WHERE id=%s;" %
                       randomDate("2017-01-01 00:00:01", "2017-10-30 23:59:59"), p['id'])

requirements = DBHelper().fetch(u'SELECT * FROM requirements;')

for i, r in enumerate(requirements):
    DBHelper().execute(u"UPDATE requirements SET added='%s' WHERE id=%s;" %
                       randomDate("2017-01-01 00:00:01", "2017-10-30 23:59:59"), r['id'])
