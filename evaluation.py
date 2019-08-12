#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from db_helper import DBHelper
from operator import attrgetter


def get_all_recommendations():
    return DBHelper().fetch(u'SELECT    * '
                            u'FROM      recommendations'
                            u'ORDER BY  id;')

def get_requirements_by_id(id):
    requirements = DBHelper().fetch(u"SELECT * FROM requirements WHERE id=%s;" % (id))

    if (len(requirements)):
        return requirements[0]

    return None

def get_requirements_distance(req_a_id, req_b_id):
    distance = DBHelper().fetch(u" SELECT * "
                                u" FROM   requirements_distance "
                                u" WHERE  req_a_id=%s "
                                u" AND    req_b_id=%s;"
                                %  (req_a_id, req_b_id))

    if (len(distance)):
        return distance[0]

    return None

def get_requirements_by_date(project_id, base_date):
    return DBHelper().fetch(u" SELECT 	    r.*"
                            u" FROM 		requirements r"
                            u" INNER JOIN   projects p ON p.code = r.code"
                            u" WHERE	    p.id = %s"
                            u" AND 		    r.added >= '%s'" % (project_id, base_date))

def insert_evaluation(recommendation_id, is_assertive):
    DBHelper().execute(u" INSERT INTO evaluations"
                     u"             (recommendation_id, is_assertive)"
                     u" VALUES      (%s, %s);"
                     % (recommendation_id, is_assertive))

def delete_all_evaluations():
    DBHelper().execute(u"TRUNCATE TABLE evaluations;")


delete_all_evaluations()
recommendations = get_all_recommendations()

for i, rec in enumerate(recommendations):
    requirement_recommended = get_requirements_by_id(rec['requirement_id'])
    requirements = get_requirements_by_date(rec['project_id'], rec['base_date'])

    is_assertive = False
    for i, req in enumerate(requirements):
        compare = get_requirements_distance(requirement_recommended['id'], requirements[i]['id'])
        if (compare is None): continue
        if (compare['distance'] <= rec['distance']): is_assertive = True

    print("rec: %s, prj: %s, assertive? %s" % (rec['id'], rec['project_id'], is_assertive))
    insert_evaluation(rec['id'], (lambda assertive: 1 if is_assertive == True else 0)(is_assertive))