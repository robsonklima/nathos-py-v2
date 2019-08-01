from google.cloud import translate
import pymysql


try:
    db = pymysql.connect(user='root', password='root', database='nhatos_v2', host='127.0.0.1')
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        # Translate projects
        sql = u"SELECT * FROM projects WHERE description_en IS NULL;"
        cursor.execute(sql)

        for i, p in enumerate(cursor.fetchall()):
            translate_client = translate.Client()
            translation = translate_client.translate(p['description'], target_language='en')

            q = u"UPDATE projects SET description_en=%s WHERE id=%s;"
            cursor.execute(q, (translation['translatedText'], p['id']))
            db.commit()

        # Translate requirements
        sql = u"SELECT * FROM requirements WHERE description_en IS NULL;"
        cursor.execute(sql)

        for i, r in enumerate(cursor.fetchall()):
            translate_client = translate.Client()
            translation = translate_client.translate(r['description'], target_language='en')

            q = u"UPDATE requirements SET description_en=%s WHERE id=%s;"
            cursor.execute(q, (translation['translatedText'], r['id']))
            db.commit()
    db.close()
except Exception as ex:
    print(ex.message)