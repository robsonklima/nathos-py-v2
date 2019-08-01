#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymysql
import random
import time


def strTimeProp(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end):
    return strTimeProp(start, end, '%Y-%m-%d %H:%M:%S', random.random())


try:
    db = pymysql.connect(user='root', password='root', database='nhatos_v2', host='127.0.0.1')
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = u"SELECT * FROM requirements;"
        cursor.execute(sql)

        for i, r in enumerate(cursor.fetchall()):
            print (randomDate("2017-01-01 00:00:01", "2019-7-01 23:59:59"))

            q = u"UPDATE requirements SET added=%s WHERE id=%s;"
            cursor.execute(q, (randomDate("2017-01-01 00:00:01", "2019-7-1 23:59:59"), r['id']))
            db.commit()

    db.close()
except Exception as ex:
    print(ex)