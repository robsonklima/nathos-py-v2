from google.cloud import translate
from db_helper import DBHelper


projects = DBHelper().fetch(u'SELECT * FROM projects WHERE description_en IS NULL;')

for i, p in enumerate(projects):
    translate_client = translate.Client()
    translation = translate_client.translate(p['description'], target_language='en')
    DBHelper.execute(u"UPDATE projects SET description_en='%s' WHERE id=%s;" %
                     (translation['translatedText'], p['id']))

requirements = DBHelper().fetch(u'SELECT * FROM requirements WHERE description_en IS NULL;')

for i, r in enumerate(requirements):
    translate_client = translate.Client()
    translation = translate_client.translate(r['description'], target_language='en')
    DBHelper.execute(u"UPDATE requirements SET description_en='%s' WHERE id=%s;" %
                     (translation['translatedText'], r['id']))
