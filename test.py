#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pandas as pd
import pymysql
import gensim
import pyemd
from nltk.corpus import stopwords
from nltk import download


try:
    dir = os.path.dirname(__file__)
    download(u'stopwords', quiet=True)
    stop_words = set(stopwords.words(u'english'))
    file = u'/data/GoogleNews-vectors-negative300.bin.gz'

    model = gensim.models.KeyedVectors.load_word2vec_format(dir + file, binary=True) #limit=500000
    model.init_sims(replace=True)

    db = pymysql.connect(user='root', password='root', database='nhatos_v2', host='127.0.0.1')
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = u"TRUNCATE TABLE requirements_distance;"
        cursor.execute(sql)

        sql = u"SELECT * FROM requirements;"
        cursor.execute(sql)
        requirements = cursor.fetchall()

        for i, req_a in enumerate(requirements):
            sentence_a = req_a['description']
            sentence_a = [w for w in sentence_a if w not in stop_words]

            for i, req_b in enumerate(requirements):
                if req_a['id'] == req_b['id']:
                    continue

                sentence_b = req_b['description']
                sentence_b = [w for w in sentence_b if w not in stop_words]

                distance = model.wmdistance(sentence_a, sentence_b)
                print(distance)

                q = u"INSERT INTO requirements_distance (req_a_id, req_b_id, distance) VALUES (%s, %s, %s);"
                cursor.execute(q, (req_a['id'], req_b['id'], distance))
                db.commit()
    db.close()
except Exception as ex:
    print(ex.message)