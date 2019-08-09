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


dir = os.path.dirname(__file__)
download(u'stopwords', quiet=True)
stop_words = set(stopwords.words(u'english'))
file = u'/data/GoogleNews-vectors-negative300.bin.gz'
model = gensim.models.KeyedVectors.load_word2vec_format(dir + file, binary=True) #limit=500000
model.init_sims(replace=True)

DBHelper().execute(u"TRUNCATE TABLE requirements_distance;")
requirements = DBHelper().fetch(u"SELECT * FROM requirements WHERE description_en IS NOT NULL;")

for i, req_a in enumerate(requirements):
    sentence_a = req_a['description_en']
    sentence_a = [w for w in sentence_a if w not in stop_words]

    for i, req_b in enumerate(requirements):
        sentence_b = req_b['description_en']
        sentence_b = [w for w in sentence_b if w not in stop_words]
        distance = model.wmdistance(sentence_a, sentence_b)

        if (distance == 0): continue

        DBHelper().execute(u"INSERT INTO requirements_distance (req_a_id, req_b_id, distance) "
                           u"VALUES (%s, %s, %s);" % (req_a['id'], req_b['id'], distance))