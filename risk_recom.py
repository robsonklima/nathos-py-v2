#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from db_helper import DBHelper
from operator import attrgetter


def get_all_projects():
    return DBHelper().fetch(u" SELECT 	  p.*"
                            u" FROM 	  projects p"
                            u" INNER JOIN risks r ON r.code = p.code"
                            u" GROUP BY	  p.id;")

def get_project_by_id(id):
    projects = DBHelper().fetch(u"SELECT * FROM projects WHERE id=%s;" % (id))

    if (len(projects)):
        return projects[0]

    return None

def get_projects_by_domain(domain):
    return DBHelper().fetch(u"SELECT * FROM projects WHERE domain='%s' ORDER BY added;" % (domain))

def get_projects_non_processed(distance, sample, steps, type):
    return DBHelper().fetch(u" SELECT     p.*" 
                            u" FROM       projects p" 
                            u" INNER JOIN risks r ON r.code = p.code"
                            u" WHERE      p.id NOT IN(" 
                            u"              SELECT project_id"
                            u"              FROM   recommendations" 
                            u"              WHERE  CAST(distance AS DECIMAL(5,1)) = %s" 
                            u"              AND    CAST(sample AS DECIMAL(5,1)) = %s" 
                            u"              AND	   CAST(steps AS DECIMAL(5,1)) = %s" 
                            u"              AND    type = '%s'"
                            u"            )"
                            u" GROUP BY   p.id"
                            u" ORDER BY   p.id ASC;" % (distance, sample, steps, type))

def get_risks_by_code(code):
    return DBHelper().fetch(u"SELECT * FROM risks WHERE code='%s';" % (code))

def get_risks_distance(risk_a_id, risk_b_id):
    distance = DBHelper().fetch(u" SELECT * "
                                u" FROM   risks_distance "
                                u" WHERE  risk_a_id=%s "
                                u" AND    risk_b_id=%s;"
                                %  (risk_a_id, risk_b_id))

    if (len(distance)):
        return distance[0]

    return None

def insert_recommendation(project_id, risk_id, base_date, distance, sample, steps, type):
    DBHelper().execute(u" INSERT INTO recommendations"
                       u"             (project_id, risk_id, base_date, distance, sample, steps, type)"
                       u" VALUES      (%s, %s, '%s', %s, %s, %s, '%s');"
                       % (project_id, risk_id, base_date, distance, sample, steps, type))

def delete_recommendations_by_type(type):
    DBHelper().execute(u"DELETE FROM recommendations WHERE type='%s';")


distance, sample, steps, counter = 0.4, 0.8, 2, 0
#delete_recommendations_by_type('RISK')
projects = get_projects_non_processed(distance, sample, steps, 'RISK')

for i, prj in enumerate(projects):
    risks = get_risks_by_code(prj['code'])
    projects_to_compare = get_projects_by_domain(prj['domain'])

    for i, pc in enumerate(projects_to_compare):
        if (prj['id'] == pc['id']): continue

        print(u'proj: %s, prj_to_compare: %s' % (prj['id'], pc['id']))

        risks_to_compare = get_risks_by_code(pc['code'])
        loop = min(int(round(len(risks) * sample)), len(risks_to_compare))

        print(u'samp: %s' % (loop))

        for i in range(loop):
            compare = get_risks_distance(risks[i]['id'], risks_to_compare[i]['id'])

            if (compare is None): continue
            if (compare['distance'] <= distance):counter += 1
            else : counter = 0

            print(u'coun: %s: ris_a: %s ris_b: %s distance: %s' %
                 (counter, risks[i]['id'],risks_to_compare[i]['id'], compare['distance']))

            if (counter == steps and i != len(risks_to_compare)):
                try:
                    counter = 0
                    insert_recommendation(prj['id'], risks_to_compare[i+1]['id'], risks[i]['added'], distance, sample, steps, 'RISK')

                    print(u'ris : %s' % risks[i + 1]['id'])
                except Exception as ex:
                    print(ex)