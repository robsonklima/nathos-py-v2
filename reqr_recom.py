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

def get_requirements_by_code(code):
    return DBHelper().fetch(u"SELECT * FROM requirements WHERE code='%s';" % (code))

def get_requirements_distance(req_a_id, req_b_id):
    distance = DBHelper().fetch(u" SELECT * "
                                u" FROM   requirements_distance "
                                u" WHERE  req_a_id=%s "
                                u" AND    req_b_id=%s;"
                                %  (req_a_id, req_b_id))

    if (len(distance)):
        return distance[0]

    return None

def insert_rec(project_id, requirement_id, base_date, distance, sample, steps, type):
    DBHelper().execute(u" INSERT INTO recommendations"
                       u"             (project_id, requirement_id, base_date, distance, sample, steps, type)"
                       u" VALUES      (%s, %s, '%s', %s, %s, %s, '%s');"
                       % (project_id, requirement_id, base_date, distance, sample, steps, type))

def delete_all_recommendations(type):
    DBHelper().execute(u"DELETE * FROM recommendations WHERE type = '%s';")


distance, sample, steps, counter = 0.3, 0.7, 3, 0
#delete_all_recommendations('REQUIREMENT')
projects = get_projects_non_processed(distance, sample, steps, 'REQUIREMENT')

for i, prj in enumerate(projects):
    requirements = get_requirements_by_code(prj['code'])
    prj_to_compare = get_projects_by_domain(prj['domain'])

    for i, pc in enumerate(prj_to_compare):
        if (prj['id'] == pc['id']): continue

        print(u'proj: %s, prj_to_compare: %s' % (prj['id'], pc['id']))

        req_to_compare = get_requirements_by_code(pc['code'])
        loop = min(int(round(len(requirements) * sample)), len(req_to_compare))

        print(u'samp: %s' % (loop))

        for i in range(loop):
            compare = get_requirements_distance(requirements[i]['id'], req_to_compare[i]['id'])

            if (compare is None): continue
            if (compare['distance'] <= distance):counter += 1
            else : counter = 0

            print(u'coun: %s: req_a: %s req_b: %s distance: %s' %
                  (counter, requirements[i]['id'], req_to_compare[i]['id'], compare['distance']))

            if (counter == steps and i != len(req_to_compare)):
                try:
                    counter = 0
                    insert_rec(prj['id'], req_to_compare[i + 1]['id'], requirements[i]['added'],
                               distance, sample, steps, 'REQUIREMENT')

                    print(u'rec : %s' % requirements[i + 1]['id'])
                except Exception as ex:
                    print(ex)



