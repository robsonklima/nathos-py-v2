#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pandas as pd
import pymysql
import gensim
import pyemd
from nltk.corpus import stopwords
from nltk import download
from db_helper import DBHelper


def delete_all_requirements_distance():
    DBHelper().execute(u"TRUNCATE TABLE requirements_distance;")

def delete_all_risks_distance():
    DBHelper().execute(u"TRUNCATE TABLE risks_distance;")

def get_all_requirements():
    return DBHelper().fetch(u"SELECT * FROM requirements WHERE description_en IS NOT NULL;")

def get_all_risks():
    return DBHelper().fetch(u"SELECT * FROM risks WHERE description_en IS NOT NULL;")

def insert_requirement_distance(req_a_id, req_b_id, distance):
    DBHelper().execute(u" INSERT INTO requirements_distance "
                       u" (req_a_id, req_b_id, distance) "
                       u" VALUES (%s, %s, %s);"
                       %  (req_a_id, req_b_id, distance))

def insert_risk_distance(risk_a_id, risk_b_id, distance):
    DBHelper().execute(u" INSERT INTO risks_distance "
                       u" (risk_a_id, risk_b_id, distance) "
                       u" VALUES (%s, %s, %s);"
                       %  (risk_a_id, risk_b_id, distance))


dir = os.path.dirname(__file__)
download(u'stopwords', quiet=True)
stop_words = set(stopwords.words(u'english'))
file = u'/data/GoogleNews-vectors-negative300.bin.gz'
model = gensim.models.KeyedVectors.load_word2vec_format(dir + file, binary=True) #limit=500000
model.init_sims(replace=True)


'''
delete_all_requirements_distance()
requirements = get_all_requirements()

try:
    for i, req_a in enumerate(requirements):
        sentence_a = req_a['description_en']
        sentence_a = [w for w in sentence_a if w not in stop_words]
    
        for i, req_b in enumerate(requirements):
            sentence_b = req_b['description_en']
            sentence_b = [w for w in sentence_b if w not in stop_words]
            distance = model.wmdistance(sentence_a, sentence_b)
    
            if (distance == 0): continue
    
            insert_requirement_distance(req_a['id'], req_b['id'], distance)
except Exception as ex:
    print(ex'''

        
delete_all_risks_distance()
risks = get_all_risks()

try:
    for i, risk_a in enumerate(risks):
        sentence_a = risk_a['description_en']
        sentence_a = [w for w in sentence_a if w not in stop_words]

        for i, risk_b in enumerate(risks):
            sentence_b = risk_b['description_en']
            sentence_b = [w for w in sentence_b if w not in stop_words]
            distance = model.wmdistance(sentence_a, sentence_b)

            if (distance == 0): continue

            insert_risk_distance(risk_a['id'], risk_b['id'], distance)
except Exception as ex:
    print(risk_a, risk_b, ex)