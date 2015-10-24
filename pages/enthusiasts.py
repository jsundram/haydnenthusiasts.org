import json


def get_context():
    performers = json.load(open('./static/data.json', 'r'))['performers']
    for performer in performers:
        performer['photo'] = u'/assets/people/' + performer['photo']
        performer['link'] = performer['name'].replace(' ', '_')

    return {
        'performers': performers
    }
