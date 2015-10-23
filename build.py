"""
Build script for site

SITE_ROOT: where we want all the compiled output to go
TEMPLATE_ROOT: where we will setup the template environment
SITE: the configuration of the site. structure is
    {
        template_file_name:
            dictionary or function that returns dictionary as a context
            for the renderer
    }
"""

from jinja2 import Environment, FileSystemLoader
from subprocess import call
import os
import pages

############################

SITE_DEPLOY = './site-deploy'
STATIC_ROOT = './static/'
TEMPLATE_ROOT = './templates'

SITE = {
    'enthusiasts.html': pages.enthusiasts,
    'about.html': None,
    'index.html': None,
    'haydn_seek.html': pages.haydn_seek
}

############################


if __name__ == "__main__":
    # first blow everything away
    print 'setting up', SITE_DEPLOY
    if os.path.exists(SITE_DEPLOY):
        call('rm -r ' + SITE_DEPLOY + '/*', shell=True)
    else:
        os.makedirs(SITE_DEPLOY)

    # copy a fresh batch of static files
    print 'copying static files'
    call(['cp', '-r', STATIC_ROOT, SITE_DEPLOY])

    # render the templates
    loader = FileSystemLoader(TEMPLATE_ROOT)
    env = Environment(loader=loader)

    for tmpl_name, context in SITE.iteritems():
        print 'building', tmpl_name
        tmpl = env.get_template(tmpl_name)
        context = context or {}
        if hasattr(context, '__call__'):
            context = context()
        # inject the name of the template in the context
        context['template_name'] = tmpl_name
        if context:
            out = tmpl.render(**context)
        else:
            out = tmpl.render()

        out_file = os.path.join(SITE_DEPLOY, tmpl_name)

        with open(out_file, 'w') as f:
            f.write(out.encode('utf-8'))

    print 'finished'
