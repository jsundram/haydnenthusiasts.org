"""
Build script for the index page
for now this is just the Haydn Seek page since there is a lot of data
that needs to be inserted, so using jinja templates to put this in
"""

from jinja2 import Template
import json

WORKS = json.load(open('../site/data.json', 'r'))['quartets']
events = [
    {
        "date": "Saturday Oct. 10",
        "time": "Morning",
        "sessions": [
            {
                "start": "8am",
                "end": "12pm",
                "location": "Shapiro Science Center Atrium",
                "performers": ["Jason", "Isaac", "Amy", "Shay"],
                "works": ["001_2", "001_3", "002_4", "002_6", "009_1", "009_6"]
            },
            {
                "start": "8:30am",
                "end": "12pm",
                "location": "Shapiro Campus Center Atrium",
                "performers": ["Susie", "Elaine", "Jon", "Josh"],
                "works": ["001_0", "001_6", "002_2", "009_3", "009_4", "017_3"]
            }
        ]
    },
    {
        "date": "Saturday Oct. 10",
        "time": "Afternoon",
        "sessions": [
            {
                "start": "2pm",
                "end": "6pm",
                "location": "Shapiro Science Center Atrium",
                "performers": ["Channing", "Aaron", "Maija", "Josh"],
                "works": ["017_2", "020_3", "020_4", "033_3", "033_4", "042"]
            },
            {
                "start": "1pm",
                "end": "5pm",
                "location": "Shapiro Campus Center Atrium",
                "performers": ["Jason", "Andrew", "Elaine", "Nicole"],
                "works": ["001_1", "001_4", "002_1", "009_2", "009_5", "017_4"]
            }
        ]
    },
    {
        "date": "Saturday Oct. 10",
        "time": "Evening",
        "sessions": [
            {
                "start": "6pm",
                "end": "10pm",
                "location": "Shapiro Science Center Atrium",
                "performers": ["Jason", "Isaac", "Elaine", "Shay"],
                "works": ["017_1", "017_6", "020_1", "020_5", "033_5", "033_6"]
            },
            {
                "start": "6pm",
                "end": "10pm",
                "location": "Shapiro Campus Center Atrium",
                "performers": ["Channing", "Andrew", "Amy", "Nicole"],
                "works": ["017_5", "020_2", "020_6", "033_1", "033_2", "050_6"]
            }
        ]
    },
    {
        "date": "Monday Oct. 12",
        "time": "Morning",
        "sessions": [
            {
                "start": "8am",
                "end": "12pm",
                "location": "Shapiro Science Center Atrium",
                "performers": ["Ryan", "Andrew", "Amy", "Nicole"],
                "works": ["050_2", "054_3", "055_2", "064_4", "064_3"]
            },
            {
                "start": "8:30am",
                "end": "12pm",
                "location": "Shapiro Campus Center Atrium",
                "performers": ["Susie", "Channing", "Jon", "Josh"],
                "works": ["050_3", "050_5", "054_1", "055_3", "064_1", "064_5"]
            }
        ]
    },
    {
        "date": "Monday Oct. 12",
        "time": "Afternoon",
        "sessions": [
            {
                "start": "1pm",
                "end": "5pm",
                "location": "Mandel Center for the Humanities",
                "performers": ["Andrew", "Ryan", "Amy", "Nicole"],
                "works": ["071_1", "074_2", "076_3", "076_6", "077_2"]
            },
            {
                "start": "1pm",
                "end": "5pm",
                "location": "Shapiro Campus Center Atrium",
                "performers": ["Jason", "Isaac", "Elaine", "Shay"],
                "works": ["050_1", "050_4", "054_2", "055_1", "064_2", "064_6"]
            }
        ]
    },
    {
        "date": "Monday Oct. 12",
        "time": "Evening",
        "sessions": [
            {
                "start": "6pm",
                "end": "8:30pm",
                "location": "Shapiro Science Center Atrium",
                "performers": ["Channing", "Susie", "Jon", "Josh"],
                "works": ["071_2", "074_3", "076_1", "076_4"]
            },
            {
                "start": "6pm",
                "end": "10pm",
                "location": "Shapiro Campus Center Atrium",
                "performers": ["Jason", "Isaac", "Elaine", "Shay"],
                "works": ["071_3", "074_1", "076_2", "076_5", "077_1", "103"]
            }
        ]
    }
]


def expand_work(work):
    # Op. 3 No. 2 Eb major "Firehose"
    work = WORKS[work]
    mode = 'major' if work['key'].istitle() else 'minor'
    nickname = work['nickname'][0] if work['nickname'] else None

    if work['#'] is not None:  # Op 42 and 103 are single works.
        base = 'Op. {opus} no. {#} {key} {mode}'.format(mode=mode, **work)
    else:
        base = 'Op. {opus} in {key} {mode}'.format(mode=mode, **work)

    if nickname:
        base += ' "{}"'.format(nickname)
    return base


def expand_works(works):
    return [expand_work(WORKS[work]) for work in works]


def get_location_class(location):
    if location == 'Shapiro Campus Center Atrium':
        return 'dot red'
    elif location == 'Shapiro Science Center Atrium':
        return 'dot blue'
    else:
        return 'dot green'

# prep data
for event in events:
    for session in event['sessions']:
        session['location_class'] = get_location_class(session['location'])
        session['works'] = [expand_work(work) for work in session['works']]


print 'building index.html'

f = open('haydn_seek_tmpl.html')
templ = Template(f.read())
f.close()
out = templ.render(events=events)

f = open('../site/index.html', 'w')
f.write(out)
f.close()

print 'finished'
