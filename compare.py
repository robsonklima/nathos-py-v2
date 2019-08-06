#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from db_helper import DBHelper
from operator import attrgetter


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

def get_all_projects():
    return DBHelper().fetch(u'SELECT * FROM projects;')

def get_projects_by_domain(domain):
    return DBHelper().fetch(u"SELECT * FROM projects WHERE domain='%s';" % (domain))

def get_requirements_by_code(code):
    return DBHelper().fetch(u"SELECT * FROM requirements WHERE code='%s';" % (code))

def get_requirements_distance(req_a_id, req_b_id):
    distance = DBHelper().fetch(u"SELECT * FROM requirements_distance WHERE req_a_id=%s AND req_b_id=%s;" % (req_a_id, req_b_id))

    if (len(distance)):
        return distance[0]

    return None


prj = get_project_by_id(12)
requirements = get_requirements_by_code(prj['code'])
projects_to_compare = get_projects_by_domain(prj['domain'])

for i, pc in enumerate(projects_to_compare):
    if (prj['id'] == pc['id']): continue

    requirements_to_compare = get_requirements_by_code(pc['code'])
    r = min(len(requirements), len(requirements_to_compare))

    for i in range(r-1):
        distance = get_requirements_distance(requirements[i]['id'], requirements_to_compare[i]['id'])

        if (distance['distance'] < 0.3): c += 1
        else : c = 0

        print(c)

        if (c == 3):
            c = 0
            print(requirements[i+1]['title'])