from google.cloud import translate
from db_helper import DBHelper


def get_all_projects():
    return DBHelper().fetch(u'SELECT * FROM projects WHERE description_en IS NULL;')

def get_all_requirements():
    return DBHelper().fetch(u'SELECT * FROM requirements WHERE description_en IS NULL;')

def update_project(translated_text, project_id):
    DBHelper.execute(u" UPDATE projects "
                     u" SET description_en='%s' WHERE id=%s;"
                     % (translated_text, project_id))

def update_requirement(translated_text, requirement_id):
    DBHelper.execute(u" UPDATE requirements "
                     u" SET description_en='%s' WHERE id=%s;"
                     % (translated_text, requirement_id))


projects = get_all_projects()

for i, p in enumerate(projects):
    translate_client = translate.Client()
    translation = translate_client.translate(p['description'], target_language='en')
    update_project(translation['translatedText'], p['id'])

requirements = get_all_requirements()

for i, r in enumerate(requirements):
    translate_client = translate.Client()
    translation = translate_client.translate(r['description'], target_language='en')
    update_requirement(translation['translatedText'], r['id'])


