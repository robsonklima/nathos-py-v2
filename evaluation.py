#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from db_helper import DBHelper
from operator import attrgetter


def get_all_recommendations():
    return DBHelper().fetch(u'SELECT * FROM recommendations;')

def get_requirements_by_id(id):
    requirements = DBHelper().fetch(u"SELECT * FROM requirements WHERE id=%s;" % (id))

    if (len(requirements)):
        return requirements[0]

    return None

def get_requirements_by_date(base_date, project_id):
    return DBHelper().fetch(u" SELECT 	    r.*"
                            u" FROM 		requirements r"
                            u" INNER JOIN   projects p ON p.code = r.code"
                            u" WHERE	    r.added >= '%s'"
                            u" AND 		    p.id = %s" % (base_date, project_id))


recommendations = get_all_recommendations()

for i, rec in enumerate(recommendations):
    requirement_recommended = get_requirements_by_id(rec['requirement_id'])
    requirements = get_requirements_by_date(rec['base_date'], rec['project_id'])

    for i, req in enumerate(requirements):
        print(req)
        # aqui tem que comparar a distancia entre o requisito recomendado e os demais requisitos do projeto
        # que ocorreram depois, considerando a distancia parametrizada durante a recomendação (rec['distance'])