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


project = get_project_by_rand()

print(project)
project_requirements = get_requirements_by_code(project['code'])

projects = get_projects_by_domain(project['domain'])

if(project):
    for i, p in enumerate(projects):
        if (project['id'] == p['id']):
            continue

        requirements = get_requirements_by_code(p['code'])
        r = min(len(project_requirements), len(requirements))

        c = 0
        for i in range(r-1):
            dis = get_requirements_distance(project_requirements[i]['id'], requirements[i]['id'])
            #print(dis)

            if (dis['distance'] < 0.3):
                c = c + 1
            else :
                c = 0

            if (c == 3):
                c = 0
                print(requirements[i+1]['title'])