#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from db_helper import DBHelper
from operator import attrgetter


def get_all_projects():
    return DBHelper().fetch(u'SELECT * FROM projects;')

def get_project_by_id(id):
    projects = DBHelper().fetch(u"SELECT * FROM projects WHERE id=%s;" % (id))

    if (len(projects)):
        return projects[0]

    return None

def get_project_by_rand():
    projects = DBHelper().fetch(u"SELECT * FROM projects ORDER BY RAND() LIMIT 1;")

    if (len(projects)):
        return projects[0]

    return None

def get_projects_by_domain(domain):
    return DBHelper().fetch(u"SELECT * FROM projects WHERE domain='%s' ORDER BY added;" % (domain))

def get_projects_non_processed(distance, sample, steps, type):
    return DBHelper().fetch(u" SELECT   p.*" 
                            u" FROM     projects p" 
                            u" WHERE    p.id NOT IN(" 
                            u"              SELECT project_id"
                            u"              FROM   recommendations" 
                            u"              WHERE  CAST(distance AS DECIMAL(5,1)) = %s" 
                            u"              AND    CAST(sample AS DECIMAL(5,1)) = %s" 
                            u"              AND	   CAST(steps AS DECIMAL(5,1)) = %s" 
                            u"              AND    type = '%s'"
                            u"          )"
                            u" ORDER BY p.id ASC" % (distance, sample, steps, type))

def get_requirements_by_project_id(project_id):
    return DBHelper().fetch(u"SELECT * FROM requirements WHERE project_id='%s';" % (project_id))

def get_requirements_distance(req_a_id, req_b_id):
    distance = DBHelper().fetch(u" SELECT * "
                                u" FROM   requirements_distance "
                                u" WHERE  req_a_id=%s "
                                u" AND    req_b_id=%s;"
                                %  (req_a_id, req_b_id))

    if (len(distance)):
        return distance[0]

    return None

def insert_recommendation(project_id, requirement_id, base_date, distance, sample, steps, type):
    DBHelper().execute(u" INSERT INTO recommendations"
                       u"             (project_id, requirement_id, base_date, distance, sample, steps, type)"
                       u" VALUES      (%s, %s, '%s', %s, %s, %s, '%s');"
                       % (project_id, requirement_id, base_date, distance, sample, steps, type))

def delete_all_recommendations(type):
    DBHelper().execute(u"DELETE * FROM recommendations WHERE type = '%s';")

def delete_recommendations(distance, sample, steps, type):
    DBHelper().execute(u" DELETE "
                       u" FROM   recommendations "
                       u" WHERE  CAST(distance AS DECIMAL(5,3))=CAST(%s AS DECIMAL(5,3))"
                       u" AND    CAST(sample AS DECIMAL(5,3))=CAST(%s AS DECIMAL(5,3))"
                       u" AND    CAST(steps AS DECIMAL(5,3))=CAST(%s AS DECIMAL(5,3))"
                       u" AND    type='%s';"
                       % (distance, sample, steps, type))


distance, steps, sample, counter, type = 0.25, 5, 0.7, 0, 'REQUIREMENT'
delete_recommendations(distance, sample, steps, type)
projects = get_projects_non_processed(distance, sample, steps, type)

for i, prj in enumerate(projects):
    try:
        requirements = get_requirements_by_project_id(prj['id'])
        prj_to_compare = get_projects_by_domain(prj['domain'])
        print(u'Processing project %s/%s' % (prj['id'], len(projects)))

        for i, pc in enumerate(prj_to_compare):
            if (prj['id'] == pc['id']): continue
            req_to_compare = get_requirements_by_project_id(pc['id'])
            loop = min(int(round(len(requirements) * sample)), len(req_to_compare)) - 1

            for i in range(loop):
                compare = get_requirements_distance(requirements[i]['id'], req_to_compare[i]['id'])
                if (compare is None): continue
                if (compare['distance'] <= distance): counter += 1
                else: counter = 0

                if (counter == steps and i != len(req_to_compare)):
                    counter = 0
                    insert_recommendation(prj['id'], req_to_compare[i + 1]['id'], requirements[i]['added'],
                                          distance, sample, steps, type)
    except Exception as ex:
        print(ex)