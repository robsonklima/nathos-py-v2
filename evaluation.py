#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from db_helper import DBHelper
from operator import attrgetter


def get_recommendations_by_type(type):
    return DBHelper().fetch(u" SELECT 	*" 
                            u" FROM 	recommendations"
                            u" WHERE	id NOT IN ("
                            u"                      SELECT recommendation_id "
                            u"                      FROM evaluations"
                            u"                     )"
                            u" AND      type='%s'"
                            u" ORDER BY id;" % type)

def get_requirement_by_id(id):
    requirements = DBHelper().fetch(u"SELECT * FROM requirements WHERE id=%s;" % (id))

    if (len(requirements)):
        return requirements[0]

    return None

def update_recommendation(recommendation_id, is_assertive):
    DBHelper().execute(u" UPDATE      recommendations"
                       u" SET         is_assertive = %s"
                       u" WHERE       id = %s;"
                       % (is_assertive, recommendation_id))

def get_risk_by_id(id):
    risks = DBHelper().fetch(u"SELECT * FROM risks WHERE id=%s;" % (id))

    if (len(risks)):
        return risks[0]

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

def get_risks_distance(risk_a_id, risk_b_id):
    distance = DBHelper().fetch(u" SELECT * "
                                u" FROM   risks_distance "
                                u" WHERE  risk_a_id=%s "
                                u" AND    risk_b_id=%s;"
                                %  (risk_a_id, risk_b_id))

    if (len(distance)):
        return distance[0]

    return None

def get_requirements_by_date(project_id, base_date):
    return DBHelper().fetch(u" SELECT 	    r.*"
                            u" FROM 		requirements r"
                            u" INNER JOIN   projects p ON p.code = r.code"
                            u" WHERE	    p.id = %s"
                            u" AND 		    r.added >= '%s'" % (project_id, base_date))

def get_risks_by_date(project_id, base_date):
    return DBHelper().fetch(u" SELECT 	    r.*"
                            u" FROM 		risks r"
                            u" INNER JOIN   projects p ON p.code = r.code"
                            u" WHERE	    p.id = %s"
                            u" AND 		    r.added >= '%s'" % (project_id, base_date))


recommendations = get_recommendations_by_type('REQUIREMENT')

for i, rec in enumerate(recommendations):
    requirements = get_requirements_by_date(rec['project_id'], rec['base_date'])

    is_assertive = False
    for i, req in enumerate(requirements):
        compare = get_requirements_distance(rec['requirement_id'], requirements[i]['id'])
        if (compare is None): continue
        if (compare['distance'] <= rec['distance']): is_assertive = True

    print("rec: %s, prj: %s, assertive? %s" % (rec['id'], rec['project_id'], is_assertive))
    update_recommendation(rec['id'], (lambda assertive: 1 if is_assertive == True else 0)(is_assertive))