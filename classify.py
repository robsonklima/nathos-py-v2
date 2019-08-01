from google.cloud import language
from operator import attrgetter
import pymysql


try:
    db = pymysql.connect(user='root', password='root', database='nhatos_v2', host='127.0.0.1')
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = u"SELECT * FROM projects;"
        cursor.execute(sql)

        for i, p in enumerate(cursor.fetchall()):
            try:
                language_client = language.LanguageServiceClient()
                document = language.types.Document(
                    content=p['description_en'],
                    type=language.enums.Document.Type.PLAIN_TEXT)
                response = language_client.classify_text(document)
                categories = response.categories

                if (len(categories) > 0):
                    category = max(categories, key=attrgetter('confidence'))
                    q = u"UPDATE projects SET domain=%s WHERE id=%s;"
                    cursor.execute(q, (category.name, p['id']))
                    db.commit()
            except Exception as ex:
                print(ex.message)
    db.close()
except Exception as ex:
    print(ex)