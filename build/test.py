# test compiler

from jinja2 import Environment, FileSystemLoader
import os

SITE_ROOT = './site-test'


def name_generator():
    return {
        'names': ['ham', 'cheese', 'marshmallows']
    }


SITE = {
    'test.html': None,
    'index.html': None
}


loader = FileSystemLoader(c'./')
env = Environment(loader=loader)

for tmpl_name, context in SITE.iteritems():
    print 'building', tmpl_name
    tmpl = env.get_template(tmpl_name)
    if hasattr(context, '__call__'):
        context = context()
    if context:
        out = tmpl.render(**context)
    else:
        out = tmpl.render()

    out_file = os.path.join(SITE_ROOT, tmpl_name)
    f = open(out_file, 'w')
    f.write(out)
    f.close()

print 'finished'
