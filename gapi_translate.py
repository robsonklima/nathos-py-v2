
projects = DbProject.get_unclassified()

for proj in projects:
    DbCategory.delete_by_project_id(proj['project_id'])
    categories = gapi_translate.classify_text(proj['description'])

    if categories:
        for category in categories:
            category_split = category['name'].split('/')

            for cat in category_split:
                if cat:
                    DbCategory.insert(proj['project_id'], cat.strip(), category['confidence'])

    DbProject.update(proj['name'], proj['description'], proj['translated'], 1, proj['project_id'])

print(u'{} Projects Classified'.format(len(projects)))
