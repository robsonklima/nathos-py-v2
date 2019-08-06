from google.cloud import language
from operator import attrgetter
from db_helper import DBHelper


try:
    projects = DBHelper().fetch(u"SELECT * FROM projects WHERE domain IS NULL OR domain = '';")

    for i, p in enumerate(projects):
        language_client = language.LanguageServiceClient()
        document = language.types.Document(content=p['description_en'],
                                           type=language.enums.Document.Type.PLAIN_TEXT)
        response = language_client.classify_text(document)
        categories = response.categories

        if (len(categories) > 0):
            category = max(categories, key=attrgetter('confidence'))
            DBHelper().execute(u"UPDATE projects SET domain='%s' WHERE id=%s;" % (category.name, p['id']))
except Exception as ex:
    print(ex)
finally:
    print(u'classify done!')