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


SITE_DEPLOY = './site-deploy'
STATIC_ROOT = './static/'
TEMPLATE_ROOT = './templates'

SITE = {
    'enthusiasts.html': pages.enthusiasts,
    'about.html': None,
    'index.html': None,
    'haydn_seek.html': pages.haydn_seek
}


def stage():
    # First, blow everything away.
    print('setting up', SITE_DEPLOY)
    if os.path.exists(SITE_DEPLOY):
        call('rm -r ' + SITE_DEPLOY + '/*', shell=True)
    else:
        os.makedirs(SITE_DEPLOY)

    # Copy a fresh batch of static files.
    print('copying static files')
    call(['cp', '-r', STATIC_ROOT, SITE_DEPLOY])


def render():
    """Render our templates."""
    loader = FileSystemLoader(TEMPLATE_ROOT)
    env = Environment(loader=loader)

    for name, context in SITE.items():
        print('building', name)
        template = env.get_template(name)

        context = context or {}
        if hasattr(context, '__call__'):
            context = context()
        # Inject template name into the context
        context['template_name'] = name

        out = template.render(**context)

        out_file = os.path.join(SITE_DEPLOY, name)

        with open(out_file, 'wb') as f:
            f.write(out.encode('utf-8'))


def main():
    stage()
    render()
    print('finished')


if __name__ == "__main__":
    main()
