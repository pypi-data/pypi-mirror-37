"""#!/usr/bin/env python
import sys
from os.path import dirname, abspath

from django.conf import settings

if not settings.configured:
    settings.configure(
        #DATABASE_ENGINE='sqlite3',
        # HACK: this fixes our threaded runserver remote tests
        # DATABASE_NAME='test_sentry',
        # TEST_DATABASE_NAME='test_sentry',
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.admin',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',

            'plugin',
            
            'plugin.tests',
        ],
        ROOT_URLCONF='',
        DEBUG=False,
        SITE_ID=1,
    )
    import djcelery
    djcelery.setup_loader()

from django.test.simple import run_tests

def runtests(*test_args):
    if 'south' in settings.INSTALLED_APPS:
        from south.management.commands import patch_for_test_db_setup
        patch_for_test_db_setup()

    if not test_args:
        test_args = ['plugin']
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)
    failures = run_tests(test_args, verbosity=1, interactive=True)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
"""
import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
test_dir = os.path.dirname(__file__)
sys.path.insert(0, test_dir)

from django.test.utils import get_runner
from django.conf import settings

import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
test_dir = os.path.dirname(__file__)
sys.path.insert(0, test_dir)

from django.test.utils import get_runner
from django.conf import settings

def runtests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['your_app'])
    sys.exit(bool(failures))
