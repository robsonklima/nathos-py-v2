#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import time
import pymysql

user, password, database, host = 'root', 'root', 'nhatos_v2', '127.0.0.1'


def strTimeProp(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end):
    return strTimeProp(start, end, '%Y-%m-%d %H:%M:%S', random.random())


try:
    db = pymysql.connect(user=user, password=password, database=database, host=host)
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        # Update projects date added randomly
        sql = u"SELECT * FROM projects;"
        cursor.execute(sql)
        projects = cursor.fetchall()

        for i, p in enumerate(projects):
            q = u"UPDATE projects SET added=%s WHERE id=%s;"
            cursor.execute(q, (randomDate("2017-01-01 00:00:01", "2017-10-30 23:59:59"), p['id']))
            db.commit()

        # Update requirements date added randomly
        sql = u"SELECT * FROM requirements;"
        cursor.execute(sql)
        requirements = cursor.fetchall()

        for i, r in enumerate(requirements):
            q = u"UPDATE requirements SET added=%s WHERE id=%s;"
            cursor.execute(q, (randomDate("2017-01-01 00:00:01", "2019-7-1 23:59:59"), r['id']))
            db.commit()
    db.close()
except Exception as ex:
    print(ex)
finally:
    print(u'random_date done!')